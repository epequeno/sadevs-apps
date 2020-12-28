module Main exposing (Msg, init, update, view)

import Browser
import Browser.Navigation exposing (back)
import Element exposing (Element, centerX, centerY, clipX, column, el, fill, fillPortion, height, layout, newTabLink, padding, paddingEach, px, rgb255, rgba255, row, scrollbarX, spacing, table, text, width)
import Element.Background
import Element.Border as Border
import Element.Font as Font
import Html exposing (Html, col, div, p)
import Html.Attributes exposing (style)
import Http
import Json.Decode as Decode exposing (Decoder, list, string)
import Json.Decode.Pipeline exposing (required)
import ParseInt exposing (parseInt)
import Time exposing (Month(..), millisToPosix, toDay, toHour, toMinute, toMonth, toYear, utc)


zeroPad : String -> String
zeroPad s =
    if String.length s == 1 then
        "0" ++ s

    else
        s


toMonthNumber : Month -> String
toMonthNumber month =
    case month of
        Jan ->
            "01"

        Feb ->
            "02"

        Mar ->
            "03"

        Apr ->
            "04"

        May ->
            "05"

        Jun ->
            "06"

        Jul ->
            "07"

        Aug ->
            "08"

        Sep ->
            "09"

        Oct ->
            "10"

        Nov ->
            "11"

        Dec ->
            "12"


toUtcString : Time.Posix -> String
toUtcString time =
    String.fromInt (toYear utc time)
        ++ "-"
        ++ zeroPad (toMonthNumber (toMonth utc time))
        ++ "-"
        ++ zeroPad (String.fromInt (toDay utc time))
        ++ " "
        ++ zeroPad
            (String.fromInt (toHour utc time))
        ++ ":"
        ++ zeroPad (String.fromInt (toMinute utc time))


timestampToUtcString : String -> String
timestampToUtcString timestamp =
    case parseInt timestamp of
        Ok n ->
            toUtcString <| millisToPosix (n * 1000)

        Err _ ->
            toUtcString <| millisToPosix 1577836800


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
    { handle : String
    , timestamp : String
    , url : String
    }


entryDecoder : Decoder Entry
entryDecoder =
    Decode.succeed Entry
        |> required "handle" string
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


backgroundColor =
    rgba255 18 18 18 100


cardBackgroundColor =
    rgba255 255 255 255 0.1


textColor =
    rgba255 255 255 255 0.9


textColorLight =
    rgba255 255 255 255 0.5


mainLayout : Model -> Html.Html msg
mainLayout model =
    layout
        [ padding 5
        , Element.Background.color backgroundColor
        ]
    <|
        row [ centerX ]
            [ mainCol model
            ]


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
        , Font.color textColor
        ]
        [ text "saved links from #library" ]


mainCol : Model -> Element msg
mainCol model =
    let
        body =
            case model.pageState of
                Loading ->
                    el [ centerX ] <| text "loading ..."

                Success ->
                    el [] <| cardsCol model.entries

                Failure ->
                    el [] <| text "failed to load data from api :("
    in
    column
        [ Font.color textColor ]
        [ header
        , body
        ]


cardUserInfo indexedEntry =
    row [ Font.size 12, Font.color textColorLight ]
        [ text "added by "
        , el [] <| text indexedEntry.user
        , text " at "
        , el [] <| text <| timestampToUtcString indexedEntry.timestamp
        ]


cardUrl indexedEntry =
    let
        url =
            indexedEntry.url

        urlText =
            if String.length url >= 80 then
                String.slice 0 80 url ++ "..."

            else
                url
    in
    row []
        [ newTabLink [] { url = url, label = text urlText }
        ]


card indexedEntry =
    el
        [ Border.widthEach { edges | bottom = 1, right = 1, left = 1, top = 1 }
        , Border.rounded 10
        , width fill
        , Element.Background.color cardBackgroundColor
        ]
    <|
        row []
            [ column
                [ paddingEach { edges | left = 5, right = 5 }
                , height fill
                , Border.widthEach { edges | right = 2 }
                , Font.color textColorLight
                ]
                [ el [ centerY ] <| text <| String.fromInt indexedEntry.index ]
            , column [ spacing 12, padding 5 ]
                [ cardUrl indexedEntry
                , cardUserInfo indexedEntry
                ]
            ]


cardsCol entries =
    column [ spacing 20 ] <| List.map card <| List.reverse <| indexedData entries


type alias IndexedEntry =
    { index : Int
    , user : String
    , timestamp : String
    , url : String
    }


toIndexedEntry : ( Int, Entry ) -> IndexedEntry
toIndexedEntry ( ix, entry ) =
    IndexedEntry ix entry.handle entry.timestamp entry.url


indexedData : List Entry -> List IndexedEntry
indexedData entries =
    entries
        |> List.reverse
        |> List.indexedMap Tuple.pair
        |> List.map toIndexedEntry
