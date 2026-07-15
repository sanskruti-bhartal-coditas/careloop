import { apiSlice } from "../../redux/slices/apiSlice";
import type { RequestOtpPayload, VerifyOtpPayload, AuthResponse, LogoutRequest } from "./Login.types";

export const loginApi = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    requestOtp: builder.mutation<void, RequestOtpPayload>({
      query: (data) => ({
        url: 'auth/request-otp',
        method: 'POST',
        body: data,
      })
    }),

    verifyOtp: builder.mutation<AuthResponse, VerifyOtpPayload>({
      query: (data) => ({
        url: 'auth/verify-otp',
        method: 'POST',
        body: data,
      })
    }),
    
    logoutUser: builder.mutation<void, LogoutRequest>({
      query: (token) => ({
        url: 'auth/logout',
        method: "POST",
        body: token
      })
    })
  })
});

export const { useRequestOtpMutation, useVerifyOtpMutation, useLogoutUserMutation } = loginApi;