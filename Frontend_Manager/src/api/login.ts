import service from "../utils/request";

// 定义 LoginData 接口
interface LoginData {
    username: string;
    password: string;
  }
  
  export function login(data: LoginData) {
    return service({
      url: '/login',
      method: 'post',
      data: data,
    });
  }

  export function tokenCheck(token: string) {
    return service({
      url: '/login',
      method: 'get',
      params: token,
    });
  }
