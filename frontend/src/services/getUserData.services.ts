import { apiSlice } from "../redux/slices/apiSlice";

interface UserDetails {
  email: string;
  role: string;
}

export const authApi = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getUserData: builder.query<UserDetails, void>({
      query: () => ({
        url: 'auth/me',
        method: 'GET',
      })
    })
  })
});

export const { useLazyGetUserDataQuery } = authApi;