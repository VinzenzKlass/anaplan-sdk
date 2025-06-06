document$.subscribe(() => {
    Promise.all([import('./assets/hljs.min.js'), import('./assets/python.min.js')]).then(([hljsModule, pyModule, pslqModule]) => {
        const hljs = hljsModule.default
        const python = pyModule.default
        hljs.configure({languages: ['python'], ignoreUnescapedHTML: true})
        hljs.registerLanguage('python', python)
        hljs.highlightAll()
    })
})
