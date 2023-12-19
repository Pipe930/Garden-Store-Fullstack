export interface Login {
  email: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface UserInfo {
  username: string;
  email: string;
  is_staff: boolean;
  is_superuser: boolean;
}
