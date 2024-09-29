import React, { useEffect } from "react";
import {
  Box,
  Button,
  Checkbox,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Stack,
} from "@chakra-ui/react";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import LoginImg from "../../assets/images/login-img-1.png";
import authApi from "../../api/authApi";
import Cookies from "js-cookie";

function Login() {
  const [show, setShow] = React.useState(false);
  const handleClick = () => setShow(!show);
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [emailError, setEmailError] = React.useState("");
  const [passwordError, setPasswordError] = React.useState("");

  const validateEmail = (email) => {
    const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return re.test(email);
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      setEmailError("Email is required");
      return null;
    }
    if (!validateEmail(email)) {
      setEmailError("Invalid email");
      return null;
    }
    if (!password) {
      setPasswordError("Password is required");
      return null;
    }

    try {
      const response = await authApi.login({
        email,
        password,
      });
      Cookies.set("access", response?.access);
      Cookies.set("refresh", response?.refresh);
      Cookies.set("role", response?.role);
      window.location.href = "/";
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {}, [emailError]);

  return (
    <Flex
      width="full"
      height="full"
      flexDirection="row"
      align="flex-start"
      className="login-page"
      maxW="calc(100vw - 400px)"
      maxH="calc(100vh - 60px)"
      m="30px auto"
    >
      <Box className="login-page__left" h="full" w="calc(100% - 100px)" mr={50}>
        <Box className="login-page__left__logo">
          <img src="https://picsum.photos/192/72" alt="logo" />
        </Box>
        <Box className="login-page__left__form" mt={24} mb={"auto"}>
          <Stack spacing={15}>
            <Heading fontWeight={600}>Login</Heading>
            <Box mb={15}>Login to access your travelwise account</Box>
            <Box>
              <form>
                <Stack spacing={6}>
                  <FormControl
                    variant="floating"
                    isInvalid={emailError?.length > 0}
                  >
                    <InputGroup flexDirection="column">
                      <Input
                        type="email"
                        borderRadius={4}
                        onChange={(e) => {
                          setEmail(e.target.value);
                          setEmailError("");
                        }}
                      />
                      <FormLabel fontWeight={400}>Email</FormLabel>
                      <FormErrorMessage>{emailError}</FormErrorMessage>
                    </InputGroup>
                  </FormControl>
                  <FormControl
                    variant="floating"
                    isInvalid={passwordError?.length > 0}
                  >
                    <InputGroup flexDirection="column">
                      <Input
                        type={show ? "text" : "password"}
                        borderRadius={4}
                        onChange={(e) => {
                          setPassword(e.target.value);
                          setPasswordError("");
                        }}
                      />
                      <FormLabel fontWeight={400}>Password</FormLabel>
                      <InputRightElement>
                        <Button
                          size="sm"
                          bg={"white"}
                          _hover={{ background: "white" }}
                          onClick={handleClick}
                        >
                          {show ? <ViewIcon /> : <ViewOffIcon />}
                        </Button>
                      </InputRightElement>
                      <FormErrorMessage>{passwordError}</FormErrorMessage>
                    </InputGroup>
                  </FormControl>
                  <FormControl>
                    <Flex
                      flexDirection="row"
                      justifyContent="space-between"
                      mb={5}
                    >
                      <Checkbox>Remember me</Checkbox>
                      <Box>
                        <Button
                          variant="link"
                          colorScheme="red"
                          _hover={{ textDecoration: "none" }}
                        >
                          Forgot password?
                        </Button>
                      </Box>
                    </Flex>
                  </FormControl>
                  <FormControl>
                    <Button
                      colorScheme="blue"
                      w="full"
                      onClick={(e) => handleSubmit(e)}
                    >
                      Login
                    </Button>
                    <Box textAlign="center" mt={3}>
                      Don't have an account?{" "}
                      <Link
                        href="/sign-up"
                        variant="link"
                        color="red"
                        _hover={{ textDecoration: "none" }}
                      >
                        Sign up
                      </Link>
                    </Box>
                  </FormControl>
                  <FormControl textAlign="center">
                    <Flex
                      flexDirection="column"
                      alignItems="center"
                      width="full"
                    >
                      <Box
                        padding="0 15px"
                        position="relative"
                        zIndex={1}
                        width="fit-content"
                        color="gray"
                        fontSize={14}
                        bg="white"
                      >
                        or login with
                      </Box>
                      <hr
                        style={{
                          width: "100%",
                          position: "relative",
                          top: "-10px",
                        }}
                      />
                    </Flex>
                  </FormControl>
                </Stack>
              </form>
            </Box>
          </Stack>
        </Box>
      </Box>
      <Box
        className="login-page__right"
        h="calc(100% - 60px)"
        w="calc(100% - 100px)"
        ml={50}
        my="auto"
      >
        <img
          src={LoginImg}
          alt="login-img"
          style={{ width: "100%", height: "100%" }}
        />
      </Box>
    </Flex>
  );
}

export default Login;
