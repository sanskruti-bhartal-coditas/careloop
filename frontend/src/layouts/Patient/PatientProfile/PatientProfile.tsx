import { useNavigate } from "react-router-dom";
import styles from "./PatientProfile.module.scss";
import { useUpdateProfileMutation } from "./PatientProfile.services";
import type { UpdateProfileRequest } from "./PatientProfile.types";
import { useForm } from "react-hook-form";
import type { BackendError } from "../../../types/BackendError.types";
import Form from "../../../components/Form/Form";
import FormInput from "../../../components/FormInput/FormInput";
import Button from "../../../components/Button/Button";

const PatientProfile = () => {
  const [updateProfile, updateProfileState] = useUpdateProfileMutation();
  const navigate = useNavigate();

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
          type="text"
          placeholder="Enter age..."
          rules={{ required: "*Age is required" }}
        />
        <FormInput
          name="height"
          label="Height : "
          type="text"
          placeholder="Enter height..."
          rules={{ required: "*Height is required" }}
        />

        <div>
          <Button type="submit" variant="primary" disabled={updateProfileState.isLoading}>
            {updateProfileState.isLoading ? "Upating profile..." : "Save changes"}
          </Button>

          <Button type="button" variant="secondary" onClick={handleCancel}>Cancel</Button>
        </div>
      </Form>
    </div>
  );
};

export default PatientProfile;
