import { useForm } from "react-hook-form";
import styles from "./Login.module.scss";
import type { LoginInterface } from "./Login.types";
import Form from "../../components/Form/Form";
import FormInput from "../../components/FormInput/FormInput";
import Button from "../../components/Button/Button";

const Login = () =>{

   const methods = useForm<LoginInterface>({
    defaultValues: { email: '', otp: '' },
    mode: "onChange"
  });

  const onSubmit = () =>{

  }

  return(
    <main className={styles.main}>
      <Form methods={methods} onSubmit={onSubmit} className={styles.formContainer}>
        <h2>Login</h2>

        <FormInput
        name="email" 
        label="Email : "
        type="email" 
        placeholder="Enter email..." 
        rules={{ required: "*Email is required" }}
      />
        <FormInput
        name="otp" 
        label="OTP : "
        type="otp" 
        placeholder="Enter OTP..." 
        rules={{ required: "*OTP is required" }}
      />

      <Button type="submit" variant="primary">
        Login
      </Button>
      </Form>
    </main>
  )
}

export default Login;