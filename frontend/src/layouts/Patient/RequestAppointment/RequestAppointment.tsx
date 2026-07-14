import styles from "./RequestAppointment.module.scss"
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import type { BackendError } from "../../../types/BackendError.types";
import Form from "../../../components/Form/Form";
import FormInput from "../../../components/FormInput/FormInput";
import Button from "../../../components/Button/Button";
import { useRequestAppointmentMutation } from "./RequestAppointment.services";
import type { RequestAppointmentRequest } from "./RequestAppointment.types";
import FormSelect from "../../../components/FormSelect/FormSelect";

const PatientProfile = () => {
  const [requestAppointment, requestAppointmentState] = useRequestAppointmentMutation();
  const navigate = useNavigate();

  const methods = useForm<RequestAppointmentRequest>({
    defaultValues: {
      appointmentType: "",
      description: "",
      disease: ""
    },
    mode: "onChange"
  });

  const handleCancel = () => navigate("/patient-dashboard");

  const onSubmit = async (data: RequestAppointmentRequest) => {
    try {
      await requestAppointment(data).unwrap();
      methods.reset();
    } catch (error) {
      console.error("Failed to request appointment:", error);
    }
  };

  // mocked for now
  const appointmentTypes = [
    { label: "Regular checkup", value: "REGULAR_CHECKUP" },
    { label: "Body check up", value: "BODYCHECKUP" },
  ];

  return (
    <div className={styles.background}>
      <h2>Request Appointment</h2>

      {requestAppointmentState.isSuccess && (
        <div className={styles.successMessage}>
          Appointment is requested successfully!
        </div>
      )}

      {requestAppointmentState.isError && (
        <div className={styles.errorMessage}>
          {(requestAppointmentState.error as BackendError)?.data?.error?.message || "An unexpected error occurred."}
        </div>
      )}

      <FormSelect
          name="role"
          label="Select Appointment Type : "
          options={appointmentTypes}
          rules={{ required: "*Appointment Type is required" }}
        />

      <Form methods={methods} onSubmit={onSubmit}>
        <FormInput
          name="descriptionName"
          label="Description : "
          type="text"
          placeholder="Enter description..."
          rules={{ required: "*Description is required" }}
        />
        {/* add inputs for here later or in separate form */}
        
        <div>
          <Button type="submit" variant="primary" disabled={requestAppointmentState.isLoading}>
            {requestAppointmentState.isLoading ? "Sending request..." : "Request"}
          </Button>

          <Button type="button" variant="secondary" onClick={handleCancel}>Cancel</Button>
        </div>
      </Form>
    </div>
  );
};

export default PatientProfile;
