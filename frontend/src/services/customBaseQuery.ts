import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { BaseQueryFn, FetchArgs, FetchBaseQueryError } from "@reduxjs/toolkit/query";
import { getRefreshToken, clearTokens, setTokens, getAccessToken } from "../utils/tokens.utils";
import { logout } from "../redux/slices/authSlice";

interface RefreshResultInterface {
  accessToken: string;
  refreshToken: string;
}

// setting up mutex lock to prevent race conditions
class Mutex {
  private mutex = Promise.resolve();

  async acquire(): Promise<() => void> {
    let release: () => void;
    const next = new Promise<void>((resolve) => {
      release = resolve;
    });
    const current = this.mutex;
    this.mutex = next;
    await current;
    return release!;
  }
}

const tokenRefreshMutex = new Mutex();

export const createBaseQueryWithReauth = (baseUrl: string): BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> => {
  const baseQuery = fetchBaseQuery({
    baseUrl,
    prepareHeaders: (headers) => {
      const token = getAccessToken();
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
      return headers;
    },
  });

  return async (args, api, extraOptions) => {
    const releaseInitial = await tokenRefreshMutex.acquire();
    releaseInitial();

    let result = await baseQuery(args, api, extraOptions);

    if (result.error && result.error.status === 401) {
      const refreshToken = getRefreshToken();

      if (refreshToken) {
        const release = await tokenRefreshMutex.acquire();

        try {
          const currentToken = getAccessToken();
          const requestToken = typeof args === 'string' || !args.headers
            ? null
            : new Headers(args.headers as HeadersInit).get('Authorization');

          if (requestToken && `Bearer ${currentToken}` !== requestToken) {
            result = await baseQuery(args, api, extraOptions);
          } else {
            const refreshResult = await baseQuery(
              {
                url: 'auth/refresh',
                method: 'POST',
                body: { refreshToken: refreshToken },
              },
              api,
              extraOptions
            );

            if (refreshResult.data) {
              const refreshData = refreshResult.data as RefreshResultInterface;
              setTokens(refreshData.accessToken, refreshData.refreshToken);
              result = await baseQuery(args, api, extraOptions);
            } else {
              clearTokens();
              api.dispatch(logout());
            }
          }
        } finally {
          release();
        }
      } else {
        clearTokens();
        api.dispatch(logout());
      }
    }
    return result;
  };
};