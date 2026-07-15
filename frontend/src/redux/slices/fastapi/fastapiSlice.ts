import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQueryWithReauth } from "../../../services/fastapi/fastapi.services"

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: baseQueryWithReauth,
  tagTypes: ['Patient', 'Coordinator', 'Appointments'], 
  endpoints: () => ({}), 
});