import { useState } from "react";
import {
  Box,
  Button,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  InputGroup,
  Stack,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";

const AccountInfoForm = ({ onSubmit }) => {
  const {
    formState: { errors },
    register,
    handleSubmit,
  } = useForm();

  const [password, setPassword] = useState();

  return (
    <Box>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack gap={5}>
          <Flex gap={5}>
            <FormControl variant="floating" isInvalid={errors["firstName"]}>
              <InputGroup flexDirection="column">
                <Input
                  type="text"
                  size="lg"
                  {...register("firstName", {
                    required: "This field is require!",
                  })}
                />
                <FormLabel fontWeight={400}>First Name</FormLabel>
                <FormErrorMessage>
                  {errors["firstName"]?.message}
                </FormErrorMessage>
              </InputGroup>
            </FormControl>
            <FormControl variant="floating" isInvalid={errors["lastName"]}>
              <InputGroup flexDirection="column">
                <Input
                  type="text"
                  size="lg"
                  {...register("lastName", {
                    required: "This field is require!",
                  })}
                />
                <FormLabel fontWeight={400}>Last Name</FormLabel>
                <FormErrorMessage>
                  {errors["lastName"]?.message}
                </FormErrorMessage>
              </InputGroup>
            </FormControl>
          </Flex>
          <Flex gap={5}>
            <FormControl variant="floating" isInvalid={errors["email"]}>
              <InputGroup flexDirection="column">
                <Input
                  type="text"
                  size="lg"
                  {...register("email", {
                    required: "This field is require!",
                    pattern: {
                      value: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
                      message: "Invalid email!",
                    },
                  })}
                />
                <FormLabel fontWeight={400}>Email</FormLabel>
                <FormErrorMessage>{errors["email"]?.message}</FormErrorMessage>
              </InputGroup>
            </FormControl>
            <FormControl variant="floating" isInvalid={errors["phoneNumber"]}>
              <InputGroup flexDirection="column">
                <Input
                  type="text"
                  size="lg"
                  {...register("phoneNumber", {
                    required: "This field is require!",
                  })}
                />
                <FormLabel fontWeight={400}>Phone Number</FormLabel>
                <FormErrorMessage>
                  {errors["phoneNumber"]?.message}
                </FormErrorMessage>
              </InputGroup>
            </FormControl>
          </Flex>
          <FormControl variant="floating" isInvalid={errors["password"]}>
            <InputGroup flexDirection="column">
              <Input
                type="password"
                size="lg"
                {...register("password", {
                  required: "This field is require!",
                  minLength: {
                    value: 6,
                    message: "Password must be at least 6 characters",
                  },
                })}
                onChange={(event) => setPassword(event.target.value)}
              />
              <FormLabel fontWeight={400}>Password</FormLabel>
              <FormErrorMessage>{errors["password"]?.message}</FormErrorMessage>
            </InputGroup>
          </FormControl>
          <FormControl
            variant="floating"
            isInvalid={errors["confirm-password"]}
          >
            <InputGroup flexDirection="column">
              <Input
                type="password"
                size="lg"
                {...register("confirm-password", {
                  required: "This field is require!",
                  validate: (value) =>
                    value === password || "Confirm password do not match!",
                })}
              />
              <FormLabel fontWeight={400}>Confirm Password</FormLabel>
              <FormErrorMessage>
                {errors["confirm-password"]?.message}
              </FormErrorMessage>
            </InputGroup>
          </FormControl>
          <FormControl>
            <Button type="submit" size="lg" width="full" colorScheme="blue">
              Next Step
            </Button>
          </FormControl>
        </Stack>
      </form>
    </Box>
  );
};

export default AccountInfoForm;
