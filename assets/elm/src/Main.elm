module Main exposing (Msg, init, update, view)

import Browser
import Html exposing (Html)
import Layout exposing (mainLayout)
import Model exposing (Entry, Model)


main : Program () Model Msg
main =
    Browser.sandbox
        { init = init
        , view = view
        , update = update
        }


entries : List Entry
entries =
    [ Entry "alice" "2020-01-01" "https://example.com"
    ]


init : Model
init =
    Model entries


type Msg
    = NoOp


update : Msg -> Model -> Model
update msg model =
    case msg of
        NoOp ->
            model


view : Model -> Html Msg
view model =
    mainLayout model
