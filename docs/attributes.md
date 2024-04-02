
# Element Attributes

All attributes can be given the value `inherit` next to the possible values given below, which means the value is copied from its parent (if there is a parent). Below is a table with all allowed attributes with a description on how to use them:

| Name | Possible values | Description |
| --- | --- | --- |
| `background-color` | `none` or a color | Set the background color of an element. |
| `continue` | `none`, `x`, `y` or `xy` | How to continue rendering after current element has been rendered. Mainly intended for internal use. |
| `font` | `default` or a `.ttf` file path | The font to give text in this element and its children. |
| `font-size` | A value | The font size in pixels. |
| `height` | `auto`, a percentage or a value | Set the height of the element. For `auto` this is the height of the child elements combined. A percentage is a proportion of the parent. A value is in pixels. |
| `max-height` | A percentage or a value | The maximum height that an element should be, which can be combined with `height="auto"`. Defaults to `1000000` |
| `max-width` | A percentage or a value | The maximum width that an element should be, which can be combined with `width="auto"`. Defaults to `1000000` |
| `min-height` | A percentage or a value | The minimum height that an element should be, which can be combined with `height="auto"`. Defaults to `0` for all elements except `col`, where the default is `100%`. |
| `min-width` | A percentage or a value | The minimum width that an element should be, which can be combined with `width="auto"`. Defaults to `0` for all elements except `text` and `row`, where the default is `100%`. |
| `render-text` | `true` or `false` | Wether the element should render text or child elements, mainly for internal use. |
| `text-align` | `left`, `center` or `right` | Where to align the text in the parent element. |
| `text-color` | A color | The color to give the text in this element and its children. |
| `width` | `auto`, a percentage or a value | Set the width of the element. For `auto` this is the width of the child elements combined. A percentage is a proportion of the parent. A value is in pixels. |
| `x` | `auto` or a value | Fixes the (global) x-coordinate of the top-left corner of the element. |
| `y` | `auto` or a value | Fixes the (global) y-coordinate of the top-left corner of the element. |