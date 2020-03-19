module Main exposing (Msg, init, update, view)

import Browser
import Element exposing (Element, centerX, column, fill, layout, paddingEach, row, table, text)
import Html exposing (Html)
import Http
import Json.Decode as Decode exposing (Decoder, field, int, list, map5, string)
import Json.Decode.Pipeline exposing (hardcoded, optional, required)


main : Program () Model Msg
main =
    Browser.document
        { init = init
        , view = view
        , update = update
        , subscriptions = \_ -> Sub.none
        }


entryDecoder : Decoder Entry
entryDecoder =
    Decode.succeed Entry
        |> required "user" string
        |> required "added_at" string
        |> required "url" string


entriesResponseDecoder : Decoder EntriesResponse
entriesResponseDecoder =
    Decode.succeed EntriesResponse
        |> required "items" (list entryDecoder)


readDb : Cmd Msg
readDb =
    Http.get
        { url = "https://api.sadevs.app"
        , expect = Http.expectJson GotJson entriesResponseDecoder
        }


type alias Model =
    { entries : List Entry
    , pageState : PageState
    }


type alias EntriesResponse =
    { items : List Entry }


type alias Entry =
    { user : String
    , added_at : String
    , url : String
    }


type PageState
    = Failure
    | Loading
    | Success EntriesResponse


init : () -> ( Model, Cmd Msg )
init _ =
    ( Model [] Loading, readDb )


type Msg
    = GotJson (Result Http.Error EntriesResponse)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotJson result ->
            case result of
                Ok entResp ->
                    ( { model | entries = entResp.items, pageState = Success entResp }, Cmd.none )

                Err _ ->
                    ( { model | pageState = Failure }, Cmd.none )


type alias Document msg =
    { title : String
    , body : List (Html msg)
    }


view : Model -> Document Msg
view model =
    let
        title =
            case model.pageState of
                Loading ->
                    "loading..."

                Success _ ->
                    "satx.dev/slack/#library"

                Failure ->
                    "json failure"
    in
    { title = title
    , body = [ mainLayout model ]
    }


mainLayout : Model -> Html.Html msg
mainLayout model =
    layout [] <| mainCol model


edges =
    { top = 0
    , bottom = 0
    , left = 0
    , right = 0
    }


header =
    row
        [ paddingEach { edges | bottom = 10, top = 10 }
        , centerX
        ]
        [ text "saved links from #library" ]


mainCol : Model -> Element msg
mainCol model =
    column
        [ centerX
        ]
        [ header
        , entryTable model.entries
        ]


entryTable : List Entry -> Element msg
entryTable entries =
    table []
        { data = entries
        , columns =
            [ { header = text "user name"
              , width = fill
              , view = \e -> text e.user
              }
            , { header = text "created at"
              , width = fill
              , view = \e -> text e.added_at
              }
            , { header = text "url"
              , width = fill
              , view = \e -> text e.url
              }
            ]
        }
