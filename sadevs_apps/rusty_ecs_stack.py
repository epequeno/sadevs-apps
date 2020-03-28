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
)

# local


class RustyEcsStack(core.Stack):
    def __init__(
        self, scope: core.Construct, id: str, dynamodb_table, ecr_repository, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        public_subnet = ec2.SubnetConfiguration(
            name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
        )

        self._vpc = ec2.Vpc(
            self,
            "RustyVpc",
            cidr="10.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True,
            max_azs=1,
            subnet_configuration=[public_subnet],
        )

        self._cluster = ecs.Cluster(self, "RustyEcsCluster", vpc=self._vpc)

        self._task_definition = ecs.FargateTaskDefinition(
            self, "RustyEcsTaskDef", cpu=256, memory_limit_mib=512
        )

        self._container_image = ecs.ContainerImage.from_ecr_repository(ecr_repository)

        self._task_definition.add_container(
            "RustyContainer", image=self._container_image
        )

        self._service = ecs.FargateService(
            self,
            "RustyFargateService",
            task_definition=self._task_definition,
            cluster=self._cluster,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        ecr_repository.grant_pull(self._task_definition.execution_role)
        dynamodb_table.grant_read_write_data(self._task_definition.execution_role)
