module Main exposing (Msg, init, update, view)

import Browser
import Element exposing (Element, centerX, column, el, fill, layout, newTabLink, padding, paddingEach, row, spacing, table, text)
import Element.Border as Border
import Element.Font as Font
import Html exposing (Html)
import Http
import Json.Decode as Decode exposing (Decoder, list, string)
import Json.Decode.Pipeline exposing (required)


httpErrorToString : Http.Error -> String
httpErrorToString error =
    case error of
        Http.BadUrl text ->
            "Bad Url: " ++ text

        Http.Timeout ->
            "Http Timeout"

        Http.NetworkError ->
            "Network Error, maybe CORS headers?"

        Http.BadStatus _ ->
            "Bad Http Status"

        _ ->
            "Other Http error"


main : Program () Model Msg
main =
    Browser.document
        { init = init
        , view = view
        , update = update
        , subscriptions = \_ -> Sub.none
        }


type alias Entry =
    { user : String
    , timestamp : String
    , url : String
    }


entryDecoder : Decoder Entry
entryDecoder =
    Decode.succeed Entry
        |> required "user" string
        |> required "timestamp" string
        |> required "url" string


type alias EntriesResponse =
    { items : List Entry }


type Msg
    = GotJson (Result Http.Error EntriesResponse)


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
    , httpErrorString : String
    }


type PageState
    = Failure
    | Loading
    | Success


init : () -> ( Model, Cmd Msg )
init _ =
    ( Model [] Loading "", readDb )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotJson result ->
            case result of
                Ok resp ->
                    ( { model | entries = resp.items, pageState = Success }, Cmd.none )

                Err e ->
                    ( { model | pageState = Failure, httpErrorString = httpErrorToString e }, Cmd.none )


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

                Success ->
                    "satx.dev/slack/#library"

                Failure ->
                    "fail: " ++ model.httpErrorString
    in
    { title = title
    , body = [ mainLayout model ]
    }


mainLayout : Model -> Html.Html msg
mainLayout model =
    layout [ padding 5 ] <| mainCol model


edges : { top : Int, bottom : Int, left : Int, right : Int }
edges =
    { top = 0
    , bottom = 0
    , left = 0
    , right = 0
    }


header : Element msg
header =
    row
        [ paddingEach { edges | bottom = 20, top = 10 }
        , centerX
        , Font.size 30
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


styledHeader headerText =
    el
        [ Font.size 20
        , Font.center
        , Font.bold
        , Border.widthEach { edges | bottom = 1 }
        , paddingEach { edges | bottom = 5 }
        ]
    <|
        text headerText


timestampCell cellText =
    el
        [ Border.widthEach { edges | bottom = 1, left = 1 }
        , padding 8
        , Font.center
        ]
    <|
        text cellText


indexCell cellText =
    el
        [ Border.widthEach { edges | bottom = 1, left = 1 }
        , padding 8
        ]
    <|
        text cellText


userCell cellText =
    el
        [ Border.widthEach { edges | bottom = 1, left = 1 }
        , padding 8
        , Font.center
        ]
    <|
        text cellText


urlCell cellText =
    el
        [ Border.widthEach { edges | bottom = 1, right = 1, left = 1 }
        , padding 8
        , Font.center
        ]
    <|
        newTabLink [] { url = cellText, label = text cellText }


type alias IndexedEntry =
    { index : Int
    , user : String
    , timestamp : String
    , url : String
    }


toIndexedEntry ( ix, entry ) =
    IndexedEntry ix entry.user entry.timestamp entry.url


indexedData entries =
    List.map toIndexedEntry <| List.indexedMap Tuple.pair <| List.reverse entries


getDate timestamp =
    case List.head <| String.split "." timestamp of
        Just datetime ->
            case List.head (String.split "T" datetime) of
                Just date ->
                    date

                Nothing ->
                    ""

        Nothing ->
            ""


getTime timestamp =
    case List.head <| String.split "." timestamp of
        Just datetime ->
            case List.head <| List.reverse (String.split "T" datetime) of
                Just date ->
                    date

                Nothing ->
                    ""

        Nothing ->
            ""


makeFormattedTimestamp timestamp =
    getDate timestamp ++ " " ++ getTime timestamp


entryTable : List Entry -> Element msg
entryTable entries =
    table [ Font.size 14 ]
        { data = List.reverse <| indexedData entries
        , columns =
            [ { header = styledHeader " "
              , width = Element.px 25
              , view = \e -> indexCell <| String.fromInt e.index
              }
            , { header = styledHeader "user"
              , width = fill
              , view = \e -> userCell e.user
              }
            , { header = styledHeader "timestamp"
              , width = fill
              , view = \e -> userCell e.timestamp
              }
            , { header = styledHeader "url"
              , width = fill
              , view = \e -> urlCell e.url
              }
            ]
        }
