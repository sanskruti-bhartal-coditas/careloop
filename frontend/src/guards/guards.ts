import type { Predicate } from "../router/router";
import { getAccessToken } from "../utils/tokens.utils";
import { store } from "../redux/store/store";

export const isUserLoggedIn: Predicate = () => {
  const token = getAccessToken();
  if(token){
    return true
  }else{
    return false
  }
};

export const isGuest: Predicate = () => {
  const token = getAccessToken();
  if(token){
    return false
  }else{
    return true
  }
};

export const hasGrantedAccess = (role: "PATIENT" | "COORDINATOR" | "ADMIN") => {
  return () => {
    const currentUser = store.getState().auth.user;
    return currentUser?.role === role;
  };
};