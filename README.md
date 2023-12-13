# maplibre-precomposed-i18n
Precomposed MapLibre fonts for better internationalization of map labels

## Examples

### Global

Global examples using the following fonts:

NotoSansBalinese-Regular.ttf, NotoSansBengali-Regular.ttf, NotoSansBuginese-Regular.ttf, NotoSansCanadianAboriginal-Regular.ttf, NotoSansCherokee-Regular.ttf, NotoSansCoptic-Regular.ttf, NotoSansDevanagari-Regular.ttf, NotoSansEthiopic-Regular.ttf, NotoSansGeorgian-Regular.ttf, NotoSansGlagolitic-Regular.ttf, NotoSansGujarati-Regular.ttf, NotoSansGurmukhi-Regular.ttf, NotoSansJavanese-Regular.ttf, NotoSansKannada-Regular.ttf, NotoSansKhmer-Regular.ttf, NotoSansLao-Regular.ttf, NotoSansLisu-Regular.ttf, NotoSansMalayalam-Regular.ttf, NotoSansMath-Regular.ttf, NotoSansMeeteiMayek-Regular.ttf, NotoSansMongolian-Regular.ttf, NotoSansMyanmar-Regular.ttf, NotoSansNewTaiLue-Regular.ttf, NotoSansNKo-Regular.ttf, NotoSansOlChiki-Regular.ttf, NotoSansOriya-Regular.ttf, NotoSans-Regular.ttf, NotoSansRunic-Regular.ttf, NotoSansSinhala-Regular.ttf, NotoSansSundanese-Regular.ttf, NotoSansSylotiNagri-Regular.ttf, NotoSansSymbols2-Regular.ttf, NotoSansSymbols-Regular.ttf, NotoSansSyriac-Regular.ttf, NotoSansTagalog-Regular.ttf, NotoSansTaiLe-Regular.ttf, NotoSansTamil-Regular.ttf, NotoSansTelugu-Regular.ttf, NotoSansThaana-Regular.ttf, NotoSansThai-Regular.ttf, NotoSansTibetan-Regular.ttf, NotoSansTifinagh-Regular.ttf

https://wipfli.github.io/maplibre-precomposed-i18n/examples/global/

<a href="https://wipfli.github.io/maplibre-precomposed-i18n/examples/global/"><img src="examples/global/screenshot.png"></a>

The following style.json should work with any version of MapLibre:

https://wipfli.github.io/maplibre-precomposed-i18n/examples/global/style.json

If you want to see the map in a particular language, you can use the following snippet in your browser console:

```js
map.setLayoutProperty("labels", "text-field", ["get", "@name:hi"])
```

This will show all labels in Hindi.
