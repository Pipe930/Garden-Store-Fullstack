export interface ResetPassword {
  email: string;
}

export interface ResetPasswordConfirm{

  uid: string;
  token: string;
  new_password: string;
  re_new_password: string;
}
