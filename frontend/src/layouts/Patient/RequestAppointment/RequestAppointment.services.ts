import { apiSlice } from "../../../redux/slices/apiSlice";
import type { RequestAppointmentRequest } from "./RequestAppointment.types";

export const requestAppointmentApi = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    requestAppointment: builder.mutation<void, RequestAppointmentRequest>({
      query: (data) => ({
        // might change later
        url: 'request-appointment',
        method: 'POST',
        body: data,
      })
    }),

  })
});

export const { useRequestAppointmentMutation } = requestAppointmentApi;