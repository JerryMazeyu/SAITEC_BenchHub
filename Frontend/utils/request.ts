import request from "axios"

//基本请求体
const service = request.create({
    baseURL:"http://localhost:5000",
});

export default service