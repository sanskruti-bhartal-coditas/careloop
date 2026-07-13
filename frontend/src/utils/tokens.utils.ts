export const setTokens = (accessToken: string, refreshToken?: string) => {
  localStorage.setItem('accessToken', JSON.stringify(accessToken));
  
  if (refreshToken) {
    localStorage.setItem('refreshToken', JSON.stringify(refreshToken));
  }
};

export const getAccessToken = (): string | null => {
  const token = localStorage.getItem('accessToken');
  return token ? JSON.parse(token) : null;
};

export const getRefreshToken = (): string | null => {
  const token = localStorage.getItem('refreshToken');
  return token ? JSON.parse(token) : null;
};

export const clearTokens = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};