import { createBrowserRouter, Navigate } from "react-router-dom";
import type React from "react";
import { store } from "../redux/store/store";
import { isGuest } from "../guards/guards";
import Unauthorized from "../components/Unauthorised/Unauthorised";
import Login from "../pages/Login/Login";

export type Predicate = () => boolean;

const RedirectByRole = () => {
  const currentUser = store.getState().auth.user;
  const role = currentUser?.role;

  if (role === "ADMIN") return <Navigate to="/admin-dashboard" />;
  if (role === "COORDINATOR") return <Navigate to="/coordinator-dashboard" />;
  if (role === "PATIENT") return <Navigate to="/patient-dashboard" />;

  return <Unauthorized />;
};

const canAccess = (Component: React.FC, guards: Predicate[], to: string = '/'): React.ComponentType => {
  return () => {
    if (!guards.every(guard => guard())) {
      return <Navigate to={to} />;
    }
    return <Component />;
  };
};

export const router = createBrowserRouter([
  {
    path: "/redirect",
    Component: RedirectByRole,
  },
  {
    path: "/",
    Component: canAccess(Login, [isGuest], "/redirect"),
  },
  {
    path: "/patient-dashboard",
   
  }
]);