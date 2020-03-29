"""
defines the ecs resources needed to run the rusty slack bot on fargate
see: https://github.com/epequeno/rusty

note: rusty is a legacy project and so has it's own build/deploy configuration
which is maintained outside of this project
"""
# stdlib

# 3rd party
from aws_cdk import (
    core,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_secretsmanager as secretsmanager,
    aws_logs as logs,
)

# local


class RustyEcsStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        dynamodb_table,
        slack_token_secret_arn,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self._ecr_repository = ecr.Repository(
            self,
            "RustyEcrRepo",
            repository_name="rusty",
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        public_subnet = ec2.SubnetConfiguration(
            name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
        )

        self._vpc = ec2.Vpc(
            self, "RustyVpc", max_azs=1, subnet_configuration=[public_subnet],
        )

        self._cluster = ecs.Cluster(
            self, "RustyEcsCluster", vpc=self._vpc, cluster_name="rusty",
        )

        """
        https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_secretsmanager.README.html
        The Secret construct does not allow specifying the SecretString property of the AWS::SecretsManager::Secret 
        resource (as this will almost always lead to the secret being surfaced in plain text and possibly committed 
        to your source control).
        
        If you need to use a pre-existing secret, the recommended way is to manually provision the secret in 
        AWS SecretsManager and use the Secret.fromSecretArn 
        """
        slackbot_token_secret = ecs.Secret.from_secrets_manager(
            secretsmanager.Secret.from_secret_arn(
                self, "RustySlackBotTokenSecret", secret_arn=slack_token_secret_arn,
            )
        )

        self._task_def_env_vars = {"RUST_LOG": "rusty_slackbot"}
        self._task_def_secrets = {"SLACKBOT_TOKEN_SECRET": slackbot_token_secret}

        self._task_definition = ecs.FargateTaskDefinition(
            self, "RustyEcsTaskDef", cpu=256, memory_limit_mib=512,
        )

        self._container_image = ecs.ContainerImage.from_ecr_repository(
            self._ecr_repository
        )

        self._task_definition.add_container(
            "RustyContainer",
            image=self._container_image,
            environment=self._task_def_env_vars,
            secrets=self._task_def_secrets,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="rustyFargateTask",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
        )

        self._service = ecs.FargateService(
            self,
            "RustyFargateService",
            task_definition=self._task_definition,
            cluster=self._cluster,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            assign_public_ip=True,
        )

        self._ecr_repository.grant_pull(self._task_definition.execution_role)
        dynamodb_table.grant_read_write_data(self._task_definition.execution_role)

    @property
    def ecr_repository(self):
        return self._ecr_repository

    @property
    def vpc(self):
        return self._vpc

    @property
    def cluster(self):
        return self._cluster
