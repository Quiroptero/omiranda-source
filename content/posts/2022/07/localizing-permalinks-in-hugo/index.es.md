---
title: "Cómo traducir enlaces en Hugo: una alternativa"
subtitle: "Y una palabra o dos sobre el código abierto"
date: 2022-07-04T19:40:11-05:00
lastmod: 2022-07-04T19:40:11-05:00
draft: false
summary: "Una alternativa simple para traducir enlaces en Hugo"
slug: "traducir-enlaces"
aliases:
  - "localizing-permalinks"
  - "traducir-enlaces"

tags:
  - "hugo"
  - "localización (traducción)"
  - "incluye código"

keywords:
  -
---
Al trabajar con el [modo multilingüe](https://gohugo.io/content-management/multilingual/) de [Hugo](https://gohugo.io/), surge la pregunta de si existe alguna manera simple y directa de localizar (es decir, traducir) los enlaces permanentes de las publicaciones.

No encontré una manera directa de hacerlo. Afortunadamente, sí hay una forma _simple_ de lograrlo, de la cual hablaré en esta publicación.

{{< admonition type=example title="Configuración inicial" open=false >}}
La solución propuesta en este artículo fue desarrollada con la siguiente configuración inicial, por lo que en adelante se asume así. Otras configuraciones deberían funcionar también, después de algunos pequeños ajustes (o quizás ninguno).

* **Hugo** >= `0.101`{{< line_break >}}Estoy seguro de que hay una versión anterior con la que se puede lograr lo mismo.
* Un [sitio web de Hugo](https://gohugo.io/commands/hugo_new_site/).
* Un [lenguaje por defecto](https://gohugo.io/content-management/multilingual/#configure-languages) previamente establecido en el archivo de configuración: ```defaultContentLanguage = <language-code>```
* Una estructura de tipo [_translation by filename_](https://gohugo.io/content-management/multilingual/#translation-by-filename).
* Algún contenido cuyo enlace permanente queremos traducir.
{{< /admonition >}}

Para este tutorial me referiré al código fuente de este mismo artículo. Se puede encontrar [aquí](https://github.com/Quiroptero/source.omiranda.dev/tree/main/content/posts/2022/07/localizing-permalinks-in-hugo).

## 1. Activar `slugorfilename` en el archivo de configuración {#activar-slugorfilename}

Dentro del [archivo de configuración](https://gohugo.io/getting-started/configuration/#configuration-file), en [la sección de _Permalinks_](https://gohugo.io/content-management/urls/#permalinks-configuration-example) establece el valor `slugorfilename` dentro del campo `posts`:

```TOML
[Permalinks]
  posts = ":slugorfilename"
```

## 2. Establecer un _slug_ en la materia frontal de los archivos {#establecer-slug}

Este artículo (y el sitio web completo) tiene dos versiones: una en inglés y otra en español. El archivo en inglés se denomina `index.en.md`, mientras que el archivo en español es `index.es.md`. Necesitamos establecer un _slug_ (esto es, la parte final del enlace) para cada uno, puesto que no es posible establecer únicamente uno de ellos y traducir el otro.

En la [materia frontal](https://gohugo.io/content-management/front-matter/) del artículo en inglés:
```YAML
slug: "localizing-permalinks"
aliases:
```

En el artículo en español:
```YAML
slug: "traducir-enlaces"
aliases:
```

Hasta ahora todo bien. Cuando el sitio sea creado, el contenido en inglés será accesible en `/localizing-permalinks/` y el contenido en español en `/es/traducir-enlaces`. Pero, ¿qué sucede si tratamos de acceder a `/traducir-enlaces/` o `/es/localizing-permalinks`?

{{< admonition type=failure title="" open=false >}}

![Error 404 al solicitar el artículo en español desde el sitio web en inglés](failure_slug_en.png "El omnipresente Error 404")

![Error 404 al solicitar el artículo en inglés desde el sitio web en español](failure_slug_es.png "")
{{< /admonition >}}

Podemos ir un paso más allá y mejorar el comportamiento del sitio web utilizando [alias](https://gohugo.io/content-management/urls/#aliases).

## 3. [Opcional] Usar alias para redireccionar al contenido traducido {#opcional-usar-alias}

Dado que estamos utilizando un enfoque de traducción por nombre de archivo, el contenido ya se encuentra enlazado por Hugo. Sin embargo, si un lector curioso (o bilingüe) trata de acceder a la correspondiente versión traducida del contenido escribiendo el enlace permanente, obtendrá un error.

Para corregir eso hacemos los siguientes cambios en las materias frontales:

`index.en.md`
```YAML
slug: "localizing-permalinks"
aliases: "traducir-enlaces"
```

`index.es.md`
```YAML
slug: "traducir-enlaces"
aliases: "localizing-permalinks"
```

De esa manera los enlaces redireccionarán adecuadamente.

## Una breve reflexión final sobre el código abierto {#going-opensource}

Inicié este sitio web hace unos pocos días (primera publicación [aquí](https://omiranda.dev/es/hola-mundo/)) y desde ese momento estuve seguro de que quería que fuera _de código abierto_. Eso significa, en corto, que el código para construir este sitio se encuentra disponible públicamente [aquí](https://github.com/Quiroptero/source.omiranda.dev).

Hay un par de razones para ello:
* Amo el código abierto. La mayoría de las cosas que sé sobre desarrollo las he aprendido de otros, ya sea leyendo artículos o navegando repositorios públicos.
* Este es un proyecto en solitario, pero eso no significa que tenga que ser un desastre. Al volverlo de código abierto me motivo a mí mismo a seguir una serie de buenas prácticas.
* Es una manera estupenda de mostrar lo que voy aprendiendo.
