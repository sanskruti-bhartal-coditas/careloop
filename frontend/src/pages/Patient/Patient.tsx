import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { clearTokens } from "../../utils/tokens.utils";
import { logout } from "../../redux/slices/authSlice";
import Sidebar from "../../components/Sidebar/Sidebar";
import Container from "../../components/Container/Container";
import type { RootState } from "../../redux/store/store";
import styles from "./Patient.module.scss";

const Patient = () => {
  // const navigate = useNavigate();
  // const dispatch = useDispatch();
  const user = useSelector((state: RootState) => state.auth.user);

  const links = [
    { label: "Request Appointment", path: "/patient/appointment" },
  ];

  const handleLogout = () => {
    // clearTokens();
    // dispatch(logout());
    // navigate("/");
  };

  return (
    <section className={styles.section}>
      <Sidebar 
        user={user?.email || "Patient"} 
        links={links} 
        onLogout={handleLogout} 
      />
      <Container />
    </section>
  );
};

export default Patient;
