document$.subscribe(() => {
    Promise.all([
        import('./assets/hljs.js'),
        import('./assets/python.js')
    ]).then(([hljsModule, pyModule]) => {
        const hljs = hljsModule.default;
        const python = pyModule.default;
        hljs.configure({
            languages: ['python'],
            ignoreUnescapedHTML: true
        });
        hljs.registerLanguage('python', python);
        const codeBlocks = document.querySelectorAll('pre code');
        for (const block of codeBlocks) {
            block.innerHTML = hljs.highlight(block.innerText, {language: 'python'}).value;
        }
    })
});
