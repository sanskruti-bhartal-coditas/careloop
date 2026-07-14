import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { useLazyGetUserDataQuery } from "../../services/getUserData.services";
import { getAccessToken, clearTokens } from "../../utils/tokens.utils";
import { saveUserData, logout } from "../../redux/slices/authSlice";
import Loader from "../Loader/Loader";

export const AuthLoader = ({ children }: { children: React.ReactNode }) => {
  const [isAuthChecking, setIsAuthChecking] = useState(true);

  const dispatch = useDispatch();
  const [getUserData] = useLazyGetUserDataQuery();

  useEffect(() => {
    const initializeAuth = async () => {
      const token = getAccessToken();

      if (token) {
        try {
          const userDetails = await getUserData().unwrap();

          dispatch(saveUserData(userDetails));
        } catch (error) {
          console.error("Session expired or invalid token", error);
          clearTokens();
          dispatch(logout());
        }
      }

      setIsAuthChecking(false);
    };

    initializeAuth();
  }, [dispatch, getUserData]); 

  if (isAuthChecking) {
    return <Loader message="Loading..." />;
  }

  return <>{children}</>;
};