export {}
const express = require('express')
const { connect } = require('../services/connect')

const userRouter = express.Router()

userRouter.get ("/", express.json({type: '*/*'}), async (req: any, rsp: any) => {
	const data = req.body

	rsp.json({'success': true})
	rsp.end
})

userRouter.post ("/", express.json({type: '*/*'}), async (req: any, rsp: any) => {
	/*<request-template>
		{
			"key":"value"
		}
	</request-template>*/

	const data = req.body

	rsp.json({'success': true})
	rsp.end
})

userRouter.put ("/", express.json({type: '*/*'}), async (req: any, rsp: any) => {
	/*<request-template>
		{
			"key":"value"
		}
	</request-template>*/

	const data = req.body

	rsp.json({'success': true})
	rsp.end
})

userRouter.delete ("/", express.json({type: '*/*'}), async (req: any, rsp: any) => {
	/*<request-template>
		{
			"key":"value"
		}
	</request-template>*/

	const data = req.body

	rsp.json({'success': true})
	rsp.end
})

module.exports = userRouter
