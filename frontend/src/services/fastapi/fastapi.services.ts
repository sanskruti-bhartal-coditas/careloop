import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { BaseQueryFn, FetchArgs, FetchBaseQueryError } from "@reduxjs/toolkit/query";
import { getRefreshToken, clearTokens, setTokens, getAccessToken } from "../../utils/tokens.utils";
import { logout } from "../../redux/slices/authSlice";

export const baseQuery = fetchBaseQuery({
  baseUrl: import.meta.env.VITE_API_BASE_URL_FASTAPI,
  prepareHeaders: (headers) => {
    const token = getAccessToken();
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
    return headers;
  },
});

interface RefreshResultInterface {
  accessToken: string;
  refreshToken: string;
}

export const baseQueryWithReauth: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (args, store, extraOptions) => {

  let result = await baseQuery(args, store, extraOptions);

  if (result.error && result.error.status === 401) {
    const refreshToken = getRefreshToken();

    if (refreshToken) {
      const refreshResult = await baseQuery(
        {
          url: 'auth/refresh',
          method: 'POST',
          body: { refreshToken: refreshToken },
        },
        store,
        extraOptions
      );

      if (refreshResult.data) {
        const refreshData = refreshResult.data as RefreshResultInterface;
        setTokens(refreshData.accessToken, refreshData.refreshToken);
        result = await baseQuery(args, store, extraOptions);
      } else {
        clearTokens();
        store.dispatch(logout());
      }
    } else {
      clearTokens();
      store.dispatch(logout());
    }

  }
  return result;
};