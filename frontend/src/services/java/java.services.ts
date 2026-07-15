import { createBaseQueryWithReauth } from "../customBaseQuery";

export const baseQueryWithReauth = createBaseQueryWithReauth(
  import.meta.env.VITE_API_BASE_URL_JAVA
);