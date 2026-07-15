import { useNavigate } from "react-router-dom";
import styles from "./PatientProfile.module.scss";
import { useUpdateProfileMutation } from "./PatientProfile.services";
import type { UpdateProfileRequest } from "./PatientProfile.types";
import { useForm } from "react-hook-form";
import type { BackendError } from "../../../types/BackendError.types";
import Form from "../../../components/Form/Form";
import FormInput from "../../../components/FormInput/FormInput";
import Button from "../../../components/Button/Button";
import { useState } from "react";
import UploadDocuments from "../UploadDocuments/UploadDocuments";

const PatientProfile = () => {
  const [updateProfile, updateProfileState] = useUpdateProfileMutation();
  const navigate = useNavigate();

  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

  const methods = useForm<UpdateProfileRequest>({
    defaultValues: {
      firstName: "",
      lastName: "",
      age: "",
      height: 0,
      weight: 0,
      phone: "",
    },
    mode: "onChange"
  });

  const handleCancel = () => navigate("/patient-dashboard");

  const onSubmit = async (data: UpdateProfileRequest) => {
    try {
      await updateProfile(data).unwrap();
      methods.reset();
    } catch (error) {
      console.error("Failed to update profile:", error);
    }
  };

  return (
    <div className={styles.background}>
      <h2>Update Profile</h2>

      {updateProfileState.isSuccess && (
        <div className={styles.successMessage}>
          Profile is updated successfully!
        </div>
      )}

      {updateProfileState.isError && (
        <div className={styles.errorMessage}>
          {(updateProfileState.error as BackendError)?.data?.error?.message || "An unexpected error occurred."}
        </div>
      )}

      <Form methods={methods} onSubmit={onSubmit}>
        <FormInput
          name="firstName"
          label="Name : "
          type="text"
          placeholder="Enter first name..."
          rules={{ required: "*First name is required" }}
        />
        <FormInput
          name="lastName"
          label="Last name : "
          type="text"
          placeholder="Enter name..."
          rules={{ required: "*Last name is required" }}
        />
        <FormInput
          name="age"
          label="Age: "
          type="number"
          placeholder="Enter age..."
          rules={{ required: "*Age is required" }}
        />
        <FormInput
          name="height"
          label="Height : "
          type="number"
          placeholder="Enter height..."
          rules={{ required: "*Height is required" }}
        />

        <FormInput
          name="weight"
          label="Weight (kg)"
          type="number"
          placeholder="Enter weight..."
          rules={{
            required: "*Weight is required",
            min: {
              value: 1,
              message: "Weight must be greater than 0",
            },
          }}
        />

        <FormInput
          name="phone"
          label="Phone Number"
          type="text"
          placeholder="Enter phone number..."
          rules={{
            required: "*Phone number is required",
            pattern: {
              value: /^[0-9]{10}$/,
              message: "Enter a valid 10-digit phone number",
            },
          }}
        />

        <div>
            <Button type="button" variant="secondary" onClick={() => setIsUploadModalOpen(true)}>
                Upload Documents
            </Button>
        </div>

        <div>
          <Button type="submit" variant="primary" disabled={updateProfileState.isLoading}>
            {updateProfileState.isLoading ? "Upating profile..." : "Save changes"}
          </Button>

          <Button type="button" variant="secondary" onClick={handleCancel}>Cancel</Button>
        </div>
      </Form>

      {isUploadModalOpen && (
        <UploadDocuments onClose={() => setIsUploadModalOpen(false)} />
      )}
    </div>
  );
};

export default PatientProfile;
