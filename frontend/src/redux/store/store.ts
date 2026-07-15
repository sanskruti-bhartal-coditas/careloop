import { combineReducers, configureStore, type UnknownAction } from "@reduxjs/toolkit";
import { authSlice } from "../slices/authSlice";
import { apiSlice } from "../slices/apiSlice";

const appReducer = combineReducers({
    auth: authSlice.reducer,
    [apiSlice.reducerPath]: apiSlice.reducer,
});

// clearing up redux store at the time of logout
const rootReducer = (state: ReturnType<typeof appReducer> | undefined, action: UnknownAction) => {
    if (action.type === 'auth/logout') {
        state = undefined;
    }
    return appReducer(state, action);
};

export const store = configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) => (
        getDefaultMiddleware().concat(apiSlice.middleware)
    )
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;