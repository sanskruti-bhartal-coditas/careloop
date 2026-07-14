export interface LoginInterface {
  email?:string,
  otp?:string
}

export interface RequestOtpPayload{
  email: string;
}
export interface SendOtpRequest{
  email: string;
}

export interface VerifyOtpRequest {
  email: string;
  otp: string;
}

export interface VerifyOtpPayload {
  email: string;
  otp: string;
}

export interface AuthResponse {
  accessToken: string;
  refreshToken: string;
}

export interface LogoutRequest {
  refreshToken: string;
}