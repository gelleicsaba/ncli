export {}
const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const userRouter = require('./controllers/user')

const PORT = 3000
const HOST_NAME = 'localhost'

const app = express()
app.use(express.static('client'))
app.use(bodyParser.urlencoded({extended: true}))

/*
app.use( (req: any, rsp: any, next: any) => {
	// specify other headers here 
	next()
})
*/

const corsOptions = {
	origin: '*',
	credentials: true,
	methods: ["GET","POST","PUT","DELETE","PATCH","HEAD"]
}
app.use( cors(corsOptions))
app.use("/user", userRouter)

app.listen(PORT, HOST_NAME, () => {
	console.log(`Server running at ${HOST_NAME}:${PORT}`)
})