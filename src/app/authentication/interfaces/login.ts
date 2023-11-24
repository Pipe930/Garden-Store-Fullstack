export interface Login {
  email: string;
  password: string;
}

export interface LoginResponse{
  access: string;
  refresh: string;
}
