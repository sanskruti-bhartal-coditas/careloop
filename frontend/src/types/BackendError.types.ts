export interface BackendError {
  data: {
    error: {
      code: string;
      message: string;
    }
  }
}