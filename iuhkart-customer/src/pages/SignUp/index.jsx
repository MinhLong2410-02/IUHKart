import React, { useCallback, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  AbsoluteCenter,
  Box,
  Divider,
  Flex,
  Heading,
  Image,
  Link,
  Stack,
  Step,
  StepDescription,
  StepIcon,
  StepIndicator,
  StepNumber,
  Stepper,
  StepSeparator,
  StepStatus,
  StepTitle,
  Text,
  useSteps,
} from "@chakra-ui/react";

import AccountInfoForm from "./AccountInfoForm";
import PersonalInfoForm from "./PersonalInfoForm";

import SignUpImg from "../../assets/images/sign-up-img-1.png";
import authApi from "../../api/authApi";

const steps = [
  {
    title: "Step 1",
    description: "Account Information",
  },
  {
    title: "Step 2",
    description: "Personal Information",
  },
];

function SignUp() {
  const navigate = useNavigate();
  const { activeStep, setActiveStep } = useSteps({
    index: 1,
    count: steps.length,
  });

  const [accountInfo, setAccountInfo] = useState({});

  const nextStep = useCallback(() => {
    setActiveStep(activeStep + 1);
  }, [activeStep, setActiveStep]);

  const handleSubmitAccountInfo = useCallback(
    (payload) => {
      setAccountInfo(payload);
      nextStep();
    },
    [setAccountInfo, nextStep]
  );

  const handleSubmitPersonalInfo = useCallback(
    async (payload) => {
      // const address = `${payload.address}, ${payload.ward}, ${payload.district}, ${payload.province}`;

      try {
        const dataRegister = {
          user: {
            email: accountInfo.email,
            password: accountInfo.password,
            address: null,
          },
          fullname: `${accountInfo.firstName} ${accountInfo.lastName}`,
          phone: accountInfo.phoneNumber,
          date_of_birth: payload.dob,
        };

        const registerResponse = await authApi.register(dataRegister);

        if (registerResponse?.customer) {
          navigate("/login");
        }
      } catch (error) {}
    },
    [accountInfo, navigate]
  );

  const renderFormByStep = useMemo(() => {
    const formByStep = {
      0: () => <AccountInfoForm onSubmit={handleSubmitAccountInfo} />,
      1: () => <PersonalInfoForm onSubmit={handleSubmitPersonalInfo} />,
    };

    return formByStep[activeStep]();
  }, [activeStep, handleSubmitAccountInfo, handleSubmitPersonalInfo]);

  return (
    <Box width="100%" height="100%" padding="100px">
      <Flex width="100%" height="100%" gap={10}>
        <Flex justifyContent="center" width="100%">
          <Image height="100%" src={SignUpImg} />
        </Flex>

        <Stack width="100%" gap={5} justifyContent="center">
          <Box>
            <Heading as="h3" size="lg">
              Sign up
            </Heading>
            <Text>
              Let’s get you all st up so you can access your personal account.
            </Text>
          </Box>
          <Box>
            <Stepper size="lg" index={activeStep} mb={5}>
              {steps.map((step, index) => (
                <Step key={index}>
                  <StepIndicator>
                    <StepStatus
                      complete={<StepIcon />}
                      incomplete={<StepNumber />}
                      active={<StepNumber />}
                    />
                  </StepIndicator>

                  <Box flexShrink="0">
                    <StepTitle style={{ fontSize: "16px" }}>
                      {step.title}
                    </StepTitle>
                    <StepDescription style={{ fontSize: "14px" }}>
                      {step.description}
                    </StepDescription>
                  </Box>

                  <StepSeparator />
                </Step>
              ))}
            </Stepper>
          </Box>

          <Box>{renderFormByStep}</Box>

          <Box textAlign="center" margin={3}>
            Already have an account?{" "}
            <Link
              variant="link"
              href="/login"
              color="red"
              _hover={{ textDecoration: "none" }}
            >
              Login
            </Link>
          </Box>

          <Box position="relative">
            <Divider />
            <AbsoluteCenter bg="white" px="4">
              or sign up with
            </AbsoluteCenter>
          </Box>
        </Stack>
      </Flex>
    </Box>
  );
}

export default SignUp;
