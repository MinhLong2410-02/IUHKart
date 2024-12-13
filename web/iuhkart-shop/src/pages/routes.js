let routes = []

const context = require.context('.', true, /route.js$/)
context.keys().forEach(key => {
    routes.push(require(`${key}`).default)
})
export default routes.flat();