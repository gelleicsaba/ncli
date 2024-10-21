export {}
const express = require('express')
const { connect } = require('../services/connect')

const userRouter = express.Router()

userRouter.get ("/", express.json ({type: '*/*'}), async (req: any, rsp: any) => {
	const data = req.body

	rsp.json ({'success': true})
	rsp.end
}

userRouter.put ("/login", express.json ({type: '*/*'}), async (req: any, rsp: any) => {
	/*<request-template>
		{
			"user":"admin",
			"pass":"qq"
		}
	</request-template>*/

	const data = req.body

	rsp.json ({'success': true})
	rsp.end
}

module.exports = userRouter
