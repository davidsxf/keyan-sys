import { http } from "@/utils/http";

export type UserResult = {
  success: boolean;
  data: {
    /** 头像 */
    avatar: string;
    /** 用户名 */
    username: string;
    /** 昵称 */
    nickname: string;
    /** 当前登录用户的角色 */
    roles: Array<string>;
    /** 按钮级别权限 */
    permissions: Array<string>;
    /** `token` */
    accessToken: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refreshToken: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

export type RefreshTokenResult = {
  success: boolean;
  data: {
    /** `token` */
    accessToken: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refreshToken: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

/** 登录 */
/** 登录接口 */
export const getLogin = (data?) => {
  // 将路径从 /api/v1/auth/login 修改为 /api/v1/users/auth/login
  console.log(data);
  return http.post<UserResult>("/api/v1/users/auth/login", {data});
};

/** 刷新token */
export const refreshTokenApi = (data?) => {
  // 将路径从 /api/v1/auth/refresh-token 修改为 /api/v1/users/auth/refresh-token
  return http.post<API.RefreshTokenResult>("/api/v1/users/auth/refresh-token", {data});
};

/** 登出接口 */
export const logoutApi = () => {
  // 将路径从 /api/v1/auth/logout 修改为 /api/v1/users/auth/logout
  return http.post<API.LoginResult>("/api/v1/users/auth/logout");
};
