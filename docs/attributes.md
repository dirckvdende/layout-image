
# Element Attributes

All attributes can be given the value `inherit` next to the possible values given below, which means the value is copied from its parent (if there is a parent). Below is a table with all allowed attributes with a description on how to use them:

| Name | Possible values | Description |
| --- | --- | --- |
| `background-color` | `none` or a color | Set the background color of an element. |
| `continue` | `none`, `x`, `y` or `xy` | How to continue rendering after current element has been rendered. Mainly intended for internal use. |
| `font` | `default` or a `.ttf` file path | The font to give text in this element and its children. |
| `font-size` | A value | The font size in pixels. |
| `height` | `auto`, a percentage or a value | Set the height of the element. For `auto` this is the height of the child elements combined. A percentage is a proportion of the parent. A value is in pixels. |
| `render-text` | `true` or `false` | Wether the element should render text or child elements, mainly for internal use. |
| `text-color` | A color | The color to give the text in this element and its children. |
| `width` | `auto`, a percentage or a value | Set the width of the element. For `auto` this is the width of the child elements combined. A percentage is a proportion of the parent. A value is in pixels. |