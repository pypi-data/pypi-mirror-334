import PleachBrandIcon from "@/assets/pleach-brand-icon.png";
import LoginBackground from "@/assets/logo-bg-1.png";
import { useLoginUser } from "@/controllers/API/queries/auth";
import { CustomLink } from "@/customization/components/custom-link";
import { ENABLE_NEW_LOGO } from "@/customization/feature-flags";
import * as Form from "@radix-ui/react-form";
import { useContext, useState } from "react";
import InputComponent from "../../components/core/parameterRenderComponent/components/inputComponent";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { SIGNIN_ERROR_ALERT } from "../../constants/alerts_constants";
import { CONTROL_LOGIN_STATE } from "../../constants/constants";
import { AuthContext } from "../../contexts/authContext";
import useAlertStore from "../../stores/alertStore";
import { LoginType } from "../../types/api";
import {
  inputHandlerEventType,
  loginInputStateType,
} from "../../types/components";

export default function LoginPage(): JSX.Element {
  const [inputState, setInputState] =
    useState<loginInputStateType>(CONTROL_LOGIN_STATE);

  const { password, username } = inputState;
  const { login } = useContext(AuthContext);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  function handleInput({
    target: { name, value },
  }: inputHandlerEventType): void {
    setInputState((prev) => ({ ...prev, [name]: value }));
  }

  const { mutate } = useLoginUser();

  function signIn() {
    const user: LoginType = {
      username: username.trim(),
      password: password.trim(),
    };

    mutate(user, {
      onSuccess: (data) => {
        login(data.access_token, "login", data.refresh_token);
      },
      onError: (error) => {
        setErrorData({
          title: SIGNIN_ERROR_ALERT,
          list: [error["response"]["data"]["detail"]],
        });
      },
    });
  }

  return (
    <Form.Root
      onSubmit={(event) => {
        if (password === "") {
          event.preventDefault();
          return;
        }
        signIn();
        const data = Object.fromEntries(new FormData(event.currentTarget));
        event.preventDefault();
      }}
      className="h-screen w-full bg-dark" // Dark theme default class applied
    >
      <div className="flex h-full w-full bg-dark">


        {/* Right Form Section */}
        <div className="flex-1 flex items-center justify-center bg-dark p-8">
          <div className="w-full max-w-md">
            {/* <img src={PleachBrandIcon} className="h-24 mx-auto" alt="Brand Logo" /> */}
            <h1 className="text-3xl text-gray-800 dark:text-gray-100 font-bold mb-6">Welcome back!</h1>

            <div className="mb-3 w-full">
              <Form.Field name="username">
                <Form.Label className="data-[invalid]:label-invalid">
                  Username <span className="font-medium text-destructive">*</span>
                </Form.Label>

                <Form.Control asChild>
                  <Input
                    type="username"
                    onChange={({ target: { value } }) => {
                      handleInput({ target: { name: "username", value } });
                    }}
                    value={username}
                    className="w-full" // Keep existing button style intact
                    required
                    placeholder="Username"
                  />
                </Form.Control>

                <Form.Message match="valueMissing" className="field-invalid text-white">
                  Please enter your username
                </Form.Message>
              </Form.Field>
            </div>

            <div className="mb-3 w-full">
              <Form.Field name="password">
                <Form.Label className="data-[invalid]:label-invalid">
                  Password <span className="font-medium text-destructive">*</span>
                </Form.Label>

                <InputComponent
                  onChange={(value) => {
                    handleInput({ target: { name: "password", value } });
                  }}
                  value={password}
                  isForm
                  password={true}
                  required
                  placeholder="Password"
                  className="w-full" // Keep existing button style intact
                />

                <Form.Message className="field-invalid text-white" match="valueMissing">
                  Please enter your password
                </Form.Message>
              </Form.Field>
            </div>

            <div className="w-full">
              <Form.Submit asChild>
                <Button className="mr-3 mt-6 w-full" type="submit">
                  Sign in
                </Button>
              </Form.Submit>
            </div>

                {/* Warning */}
                <div className="mt-5">
                  <div className="bg-yellow-500/20 text-yellow-700 px-3 py-2 rounded-sm">
                    <svg className="inline w-3 h-3 shrink-0 fill-current mr-2" viewBox="0 0 12 12">
                      <path d="M10.28 1.28L3.989 7.575 1.695 5.28A1 1 0 00.28 6.695l3 3a1 1 0 001.414 0l7-7A1 1 0 0010.28 1.28z" />
                    </svg>
                    <span className="text-sm">Its a Beta Version. Features are under development. Expected to go live by May 31st.</span>
                  </div>
                </div>  
            {/* Uncomment for Signup Link */}
            {/* <div className="w-full mt-4 text-center">
              <CustomLink to="/signup">
                <Button className="w-full" variant="outline" type="button">
                  Don't have an account?&nbsp;<b>Sign Up</b>
                </Button>
              </CustomLink>
            </div> */}
          </div>
        </div>

                {/* Left Image Section */}
                <div className="flex-1 hidden md:block bg-cover bg-center" style={{ backgroundImage: `url(${LoginBackground})` }}>
          {/* You can replace PleachBrandIcon with any other image you like */}
        </div>
      </div>
    </Form.Root>
  );
}
