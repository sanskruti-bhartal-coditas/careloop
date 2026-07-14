import { apiSlice } from "../../../redux/slices/apiSlice";
import type { UpdateProfileRequest } from "./PatientProfile.types";

export const patientProfileApi = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    updateProfile: builder.mutation<void, UpdateProfileRequest>({
      query: (data) => ({
        url: 'update-profile',
        method: 'POST',
        body: data,
      })
    }),

  })
});

export const { useUpdateProfileMutation } = patientProfileApi;