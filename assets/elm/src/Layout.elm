module Layout exposing (mainLayout)

import Element exposing (Element, centerX, column, el, fill, layout, paddingEach, row, table, text)
import Html
import Model exposing (Entry, Model)


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
              , view = \e -> text e.createdAt
              }
            , { header = text "url"
              , width = fill
              , view = \e -> text e.url
              }
            ]
        }
