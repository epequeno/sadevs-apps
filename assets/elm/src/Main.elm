module Main exposing (Model, Msg, init, update, view)

import Browser
import Button exposing (myButton)
import Html exposing (..)


main : Program () Model Msg
main =
    Browser.sandbox
        { init = init
        , view = view
        , update = update
        }


type alias Model =
    { count : Int
    }


init : Model
init =
    Model 0


type Msg
    = NoOp


update : Msg -> Model -> Model
update msg model =
    case msg of
        NoOp ->
            model


view : Model -> Html Msg
view model =
    div []
        [ text <| myButton ++ " " ++ String.fromInt model.count ]
