module Model exposing (Model, Entry)


type alias Entry =
    { user : String
    , createdAt : String
    , url : String
    }


type alias Model =
    { entries : List Entry
    }
