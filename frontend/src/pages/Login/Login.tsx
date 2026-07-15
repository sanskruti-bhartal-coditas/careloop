import { useForm } from "react-hook-form";
import styles from "./Login.module.scss";
import Button from "../../components/Button/Button";
import Form from "../../components/Form/Form";
import FormInput from "../../components/FormInput/FormInput";
import type { LoginInterface, SendOtpRequest, VerifyOtpRequest } from "./Login.types";
import { useRequestOtpMutation, useVerifyOtpMutation } from "./Login.services";
import { useState } from "react";
import { useLazyGetUserDataQuery } from "../../services/getUserData.services";
import { setTokens } from "../../utils/tokens.utils";
import { saveUserData } from "../../redux/slices/authSlice";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import type { BackendError } from "../../types/BackendError.types";

const Login = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [emailSentTo, setEmailSentTo] = useState("");

  const [requestOtp, requestOtpState] = useRequestOtpMutation();
  const [verifyOtp, verifyOtpState] = useVerifyOtpMutation();
  const [getUserData] = useLazyGetUserDataQuery();

  const methods = useForm<LoginInterface>({
    defaultValues: { email: '', otp: '' },
    mode: "onChange"
  });

  const onEmailSubmit = async () => {
    try {
      const email = methods.getValues("email")
      await requestOtp(email).unwrap();
      setEmailSentTo(email);
    } catch (err) {
      console.error("Failed to request OTP", err);
    }
  };

  const onOtpSubmit = async (data: VerifyOtpRequest) => {
    try {
      const tokenResponse = await verifyOtp(data).unwrap();
      setTokens(tokenResponse.accessToken, tokenResponse.refreshToken);

      const userDetails = await getUserData().unwrap();
      dispatch(saveUserData(userDetails));

      navigate("/redirect");
    } catch (err) {
      console.error("Failed to verify OTP", err);
    }
  };

  return (
    <section className={styles.section}>

      <Form methods={methods} onSubmit={onOtpSubmit} className={styles.formContainer}>
        <h2>Welcome to CareLoop</h2>

        {requestOtpState.isError && (
          <div className={styles.errorMessage}>
            {(requestOtpState.error as BackendError)?.data?.error?.message || "Failed to send code."}
          </div>
        )}
        {
          emailSentTo && (
            <div>Email is sent to {emailSentTo}!</div>
          )
        }

        <FormInput
          name="email"
          label="Email Address :"
          type="email"
          placeholder="patient@example.com"
          rules={{
            required: "*Email is required",
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: "*Please enter a valid email address"
            }
          }}
        />

        <Button type="button" variant="primary" disabled={requestOtpState.isLoading} onClick={onEmailSubmit}>
          {requestOtpState.isLoading ? "Sending OTP..." : "Send OTP Code"}
        </Button>

        {verifyOtpState.isError && (
          <div className={styles.errorMessage}>
            {(verifyOtpState.error as BackendError)?.data?.error?.message || "Failed to verify OTP"}
          </div>
        )}
        <FormInput
          name="otp"
          label="Enter OTP : "
          type="text"
          maxLength={6}
          rules={{
            required: "*OTP is required",
          }}
        />

        <Button type="submit" variant="primary" disabled={verifyOtpState.isLoading}>
          {verifyOtpState.isLoading ? "Verifying..." : "Log In"}
        </Button>

      </Form>

    </section>
  );
};

export default Login;