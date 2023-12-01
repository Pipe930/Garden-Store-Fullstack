export interface Register {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  password: string;
  re_password: string;
}

export interface RegisterResponse {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  id: number;
}
