export {}
const express = require ('express')
const bodyParser = require ('body-parser')
const userRouter = require ('./routes/user')

const PORT = 3000
const HOST_NAME = 'localhost'

const app = express ()
app.use (express.static ('client'))
app.use (bodyParser.urlencoded ({extended: true}))
app.use ( (req: any, rsp: any, next: any) => {
	rsp.header ("Access-Control-Allow-Origin", "*")
	rsp.header ("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH")
	rsp.header ("Access-Control-Allow-Headers", "X-Requested-With")
	next ()
})
app.use ("/user", userRouter)

app.listen (PORT, HOST_NAME, () => {
	console.log (`Server running at ${HOST_NAME}:${PORT}`)
})