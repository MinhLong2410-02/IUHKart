import {
  Box,
  Button,
  Checkbox,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  InputGroup,
  Link,
  Stack,
} from "@chakra-ui/react";
import { useState } from "react";
import { useForm } from "react-hook-form";

const PersonalInfoForm = ({ onSubmit }) => {
  const {
    formState: { errors },
    register,
    handleSubmit,
  } = useForm();

  const [isAcceptPolicy, setAcceptPolicy] = useState(false);

  return (
    <Box>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack gap={5}>
          <FormControl variant="floating" isInvalid={errors["dob"]}>
            <InputGroup flexDirection="column">
              <Input
                type="date"
                size="lg"
                {...register("dob", {
                  required: "This field is require!",
                })}
              />
              <FormLabel fontWeight={400}>Date Of Birth</FormLabel>
              <FormErrorMessage>{errors["dob"]?.message}</FormErrorMessage>
            </InputGroup>
          </FormControl>
          <Flex gap={5}>
            <FormControl variant="floating" isInvalid={errors["province"]}>
              <InputGroup flexDirection="column">
                <Input
                  type="text"
                  size="lg"
                  {...register("province", {
                    required: "This field is require!",
                  })}
                />
                <FormLabel fontWeight={400}>Province</FormLabel>
                <FormErrorMessage>
                  {errors["province"]?.message}
                </FormErrorMessage>
              </InputGroup>
            </FormControl>
            <FormControl variant="floating" isInvalid={errors["district"]}>
              <InputGroup flexDirection="column">
                <Input
                  type="text"
                  size="lg"
                  {...register("district", {
                    required: "This field is require!",
                  })}
                />
                <FormLabel fontWeight={400}>District</FormLabel>
                <FormErrorMessage>
                  {errors["district"]?.message}
                </FormErrorMessage>
              </InputGroup>
            </FormControl>
          </Flex>
          <FormControl variant="floating" isInvalid={errors["ward"]}>
            <InputGroup flexDirection="column">
              <Input
                type="text"
                size="lg"
                {...register("ward", {
                  required: "This field is require!",
                })}
              />
              <FormLabel fontWeight={400}>Ward</FormLabel>
              <FormErrorMessage>{errors["ward"]?.message}</FormErrorMessage>
            </InputGroup>
          </FormControl>
          <FormControl variant="floating" isInvalid={errors["address"]}>
            <InputGroup flexDirection="column">
              <Input
                type="text"
                size="lg"
                {...register("address", {
                  required: "This field is require!",
                })}
              />
              <FormLabel fontWeight={400}>Address</FormLabel>
              <FormErrorMessage>{errors["address"]?.message}</FormErrorMessage>
            </InputGroup>
          </FormControl>
          <Flex justifyContent="space-between" mb={5}>
            <Checkbox
              onChange={(event) => setAcceptPolicy(event.target.checked)}
            >
              I agree to all the{" "}
              <Link color="red" href="#">
                Terms
              </Link>{" "}
              and{" "}
              <Link color="red" href="#">
                Privacy Policies
              </Link>
            </Checkbox>
          </Flex>
          <FormControl>
            <Button
              type="submit"
              isDisabled={!isAcceptPolicy}
              size="lg"
              width="full"
              colorScheme="blue"
            >
              Create Account
            </Button>
          </FormControl>
        </Stack>
      </form>
    </Box>
  );
};

export default PersonalInfoForm;
