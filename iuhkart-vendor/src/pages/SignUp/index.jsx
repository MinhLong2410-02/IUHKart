import React from 'react';
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
    Select,
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
    Textarea,
    useSteps
} from "@chakra-ui/react";
import { ArrowUpDownIcon, ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import SignUpImg from "../../assets/images/signup1vendor.png";
import { Form, useNavigate } from 'react-router-dom';
import { registerAPI } from '../../api/authApi';

const steps = [
    {
        title: "Step 1",
        description: "Account Information"
    },
    {
        title: "Step 2",
        description: "Personal Information"
    }
]

function SignUp() {

    const navigate = useNavigate();

    const [showPassword, setShowPassword] = React.useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);
    const toggleShow = (currentValue, setterFunction) => {
        setterFunction(!currentValue);
    }
    const [email, setEmail] = React.useState('');
    const [shopName, setShopName] = React.useState('');
    const [phoneNumber, setPhoneNumber] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [confirmPassword, setConfirmPassword] = React.useState('');
    const [emailError, setEmailError] = React.useState('');
    const [passwordError, setPasswordError] = React.useState('')
    const [confirmPasswordError, setConfirmPasswordError] = React.useState('')
    const { activeStep, setActiveStep } = useSteps({
        index: 0,
        count: steps.length,
    })
    
    const validateFormData = (data) => {
        let valid = true;
        if (!data.email) {
            setEmailError('Email is required');
            valid = false;
        } else {
            setEmailError('');
        }
        if (!data.password) {
            setPasswordError('Password is required');
            valid = false;
        } else {
            setPasswordError('');
        }
        if (data.password !== data.confirmPassword) {
            setConfirmPasswordError('Passwords do not match');
            valid = false;
        } else {
            setConfirmPasswordError('');
        }
        return valid;
    };

    const changeStep = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);
        formData.append('confirmPassword', confirmPassword);
        formData.append('shopName', shopName);
        formData.append('phoneNumber', phoneNumber);

        const data = Object.fromEntries(formData.entries());

        const param = {
            "user": {
              "email": email,
              "password": password,
              "address": 1
            },
            "name": shopName,
            "phone": phoneNumber,
            "description": "",
        }

        if (validateFormData(data)) {

            const data = await registerAPI(param);
            if (data) {
                navigate('/sign-up-next'); 
            }
        }
    };


    return (
        <Flex
            width="full"
            height="full"
            flexDirection="row"
            align="flex-start"
            className="login-page justify-between"
        >
            <Box className="login-page__right__1 flex justify-center items-center" h="full" p={50}>
                <Flex className="login-page__right__logo" justifyContent="flex-end">
                    {/* <img src="https://picsum.photos/192/72" alt="logo"/> */}
                </Flex>
                <Box className="login-page__right__form" mt={6}>
                    <Stack spacing={15} paddingLeft={20}>
                        <Heading fontWeight={700} fontSize={50} mb={20} >Sign Up</Heading>
                        <Box className="login-page__right__form__step1">
                            <form>
                                <Stack spacing={6}>
                                    <FormControl variant="floating">
                                        <Flex>
                                            <InputGroup flexDirection="column" mr={6}>
                                                <Input 
                                                    onChange={(e) => {
                                                        setShopName(e.target.value)
                                                    }}
                                                />
                                                <FormLabel fontWeight={400}>Shop Name</FormLabel>
                                                <FormErrorMessage></FormErrorMessage>
                                            </InputGroup>
                                        </Flex>
                                    </FormControl>
                                    <FormControl variant="floating">
                                        <Flex>
                                            <InputGroup flexDirection="column" mr={3}>
                                                <Input 
                                                    onChange={(e) => {
                                                        setEmail(e.target.value)
                                                    }}
                                                />
                                                <FormLabel fontWeight={400}>Email</FormLabel>
                                                <FormErrorMessage></FormErrorMessage>
                                            </InputGroup>
                                            <InputGroup flexDirection="column" ml={3}>
                                                <Input 
                                                    onChange={(e) => {
                                                        setPhoneNumber(e.target.value)
                                                    }}
                                                />
                                                <FormLabel fontWeight={400}>Phone Number</FormLabel>
                                                <FormErrorMessage></FormErrorMessage>
                                            </InputGroup>
                                        </Flex>
                                    </FormControl>
                                    <FormControl variant="floating" isInvalid={passwordError?.length > 0}>
                                        <InputGroup flexDirection="column">
                                            <Input type={showPassword ? 'text' : 'password'} borderRadius={4}
                                                onChange={(e) => {
                                                    setPassword(e.target.value)
                                                    setPasswordError('')
                                                }} />
                                            <FormLabel fontWeight={400}>Password</FormLabel>
                                            <InputRightElement>
                                                <Button size='sm' bg={"white"} _hover={{ background: "white" }}
                                                    onClick={() => toggleShow(showPassword, setShowPassword)}>
                                                    {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                                                </Button>
                                            </InputRightElement>
                                            <FormErrorMessage>{passwordError}</FormErrorMessage>
                                        </InputGroup>
                                    </FormControl>
                                    <FormControl variant="floating" isInvalid={passwordError?.length > 0}>
                                        <InputGroup flexDirection="column">
                                            <Input type={showConfirmPassword ? 'text' : 'password'} borderRadius={4}
                                                onChange={(e) => {
                                                    setConfirmPassword(e.target.value)
                                                    setPasswordError('')
                                                }} />
                                            <FormLabel fontWeight={400}>Confirm Password</FormLabel>
                                            <InputRightElement>
                                                <Button size='sm' bg={"white"} _hover={{ background: "white" }}
                                                    onClick={() => toggleShow(showConfirmPassword, setShowConfirmPassword)}>
                                                    {showConfirmPassword ? <ViewIcon /> : <ViewOffIcon />}
                                                </Button>
                                            </InputRightElement>
                                            <FormErrorMessage>{passwordError}</FormErrorMessage>
                                        </InputGroup>
                                    </FormControl>


                                    <FormControl>
                                        <button
                                            w="full"
                                            type="submit"
                                            onClick={changeStep}
                                            className='w-[80px] h-[80px] rounded-[35px] flex justify-center items-center bg-[#FFB7D5] text-white font-bold text-lg hover:bg-[#FFB7D5] hover:text-white'
                                        ><svg width="23" height="23" viewBox="0 0 23 23" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <path d="M9.89269 1.82177L10.9938 0.692085C11.46 0.21375 12.2139 0.21375 12.6751 0.692085L22.3169 10.5794C22.7831 11.0577 22.7831 11.8312 22.3169 12.3044L12.6751 22.1968C12.2089 22.6751 11.455 22.6751 10.9938 22.1968L9.89269 21.0671C9.42151 20.5837 9.43143 19.795 9.91253 19.3217L15.889 13.4799H1.63468C0.975031 13.4799 0.444336 12.9354 0.444336 12.2586V10.6303C0.444336 9.95347 0.975031 9.40898 1.63468 9.40898H15.889L9.91253 3.56718C9.42647 3.09394 9.41655 2.30519 9.89269 1.82177Z" fill="white" />
                                            </svg>
                                        </button>
                                        <Box textAlign="start" mt={10}>
                                            Already have an account? <Link variant="link" href="/login" color="#FFB7D5"
                                                _hover={{ textDecoration: "none" }}>Login</Link>
                                        </Box>
                                    </FormControl>
                                </Stack>
                            </form>
                        </Box>


                    </Stack>
                </Box>
            </Box>
            <Box className="login-page__left flex justify-end items-end" h="100%" w="60%" >
                <img src={SignUpImg} alt="login-img" style={{ width: "100%", height: "90%" }} />
            </Box>

        </Flex>
    );
}

export default SignUp;