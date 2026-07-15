import { createSlice } from '@reduxjs/toolkit';

interface User{
  email:string,
  role:string,
  id:string
}

interface AuthState {
  user : User | null,
  isAuthenticated : boolean
}

const initialState:AuthState = {
    user: null,
    isAuthenticated: false,
  }

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    saveUserData: (state, action) => {
      state.isAuthenticated = true;
      state.user = action.payload;
    },
    logout: (state) => {
      state.isAuthenticated = false;
      state.user = null;
    },
  },
});

export const { saveUserData, logout } = authSlice.actions;

export default authSlice.reducer;