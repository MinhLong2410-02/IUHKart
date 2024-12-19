import React, { useEffect } from 'react';
import {
    Box, Button, calc, Checkbox,
    Flex,
    FormControl, FormErrorMessage, FormHelperText,
    FormLabel,
    Heading,
    Input, InputGroup,
    InputRightElement,
    Stack
} from "@chakra-ui/react";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import LoginImg from "../../assets/images/loginVendor.png"
import authApi from "../../api/authApi";
import { NavLink } from 'react-router-dom';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';


function Login() {
    const [show, setShow] = React.useState(false);
    const handleClick = () => setShow(!show);
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [emailError, setEmailError] = React.useState('');
    const [passwordError, setPasswordError] = React.useState('')
    const [loginError, setLoginError] = React.useState('');

    const validateEmail = (email) => {
        const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return re.test(email);
    }
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoginError('');

        if (!email) {
            setEmailError('Email is required');
            return null;
        }
        if (!validateEmail(email)) {
            setEmailError('Invalid email');
            return null;
        }
        if (!password) {
            setPasswordError('Password is required');
            return null;
        }

        try {
            const response = await authApi.login({
                email,
                password
            })
            // console.log(response)
            // set response.access to Cookies
            Cookies.set('authorization', response.access)
            // redirect to home page
            window.location.href = '/dashboard'

        } catch (error) {
            console.error(error);
            setLoginError('Sai email hoặc mật khẩu. Vui lòng thử lại');
        }
    }

    useEffect(() => {
    }, [emailError])

    return (
        <Flex
            width="full"
            height="full"
            flexDirection="row"
            align="flex-start"
            className="login-page flex justify-center items-center"
        >
            <Box className="login-page__left" h="full" w="calc(100% - 100px)" p={20}>
                <Box className="login-page__left__logo">
                    <svg width="66" height="29" viewBox="0 0 66 29" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M14.6152 18.5723V22H3.87793V18.5723H14.6152ZM5.29883 0.671875V22H0.904297V0.671875H5.29883ZM16.1973 14.2363V13.9287C16.1973 12.7666 16.3633 11.6973 16.6953 10.7207C17.0273 9.73438 17.5107 8.87988 18.1455 8.15723C18.7803 7.43457 19.5615 6.87305 20.4893 6.47266C21.417 6.0625 22.4814 5.85742 23.6826 5.85742C24.8838 5.85742 25.9531 6.0625 26.8906 6.47266C27.8281 6.87305 28.6143 7.43457 29.249 8.15723C29.8936 8.87988 30.3818 9.73438 30.7139 10.7207C31.0459 11.6973 31.2119 12.7666 31.2119 13.9287V14.2363C31.2119 15.3887 31.0459 16.458 30.7139 17.4443C30.3818 18.4209 29.8936 19.2754 29.249 20.0078C28.6143 20.7305 27.833 21.292 26.9053 21.6924C25.9775 22.0928 24.9131 22.293 23.7119 22.293C22.5107 22.293 21.4414 22.0928 20.5039 21.6924C19.5762 21.292 18.79 20.7305 18.1455 20.0078C17.5107 19.2754 17.0273 18.4209 16.6953 17.4443C16.3633 16.458 16.1973 15.3887 16.1973 14.2363ZM20.416 13.9287V14.2363C20.416 14.9004 20.4746 15.5205 20.5918 16.0967C20.709 16.6729 20.8945 17.1807 21.1484 17.6201C21.4121 18.0498 21.7539 18.3867 22.1738 18.6309C22.5938 18.875 23.1064 18.9971 23.7119 18.9971C24.2979 18.9971 24.8008 18.875 25.2207 18.6309C25.6406 18.3867 25.9775 18.0498 26.2314 17.6201C26.4854 17.1807 26.6709 16.6729 26.7881 16.0967C26.915 15.5205 26.9785 14.9004 26.9785 14.2363V13.9287C26.9785 13.2842 26.915 12.6787 26.7881 12.1123C26.6709 11.5361 26.4805 11.0283 26.2168 10.5889C25.9629 10.1396 25.626 9.78809 25.2061 9.53418C24.7861 9.28027 24.2783 9.15332 23.6826 9.15332C23.0869 9.15332 22.5791 9.28027 22.1592 9.53418C21.749 9.78809 21.4121 10.1396 21.1484 10.5889C20.8945 11.0283 20.709 11.5361 20.5918 12.1123C20.4746 12.6787 20.416 13.2842 20.416 13.9287ZM43.8389 6.15039H47.6621V21.4727C47.6621 22.918 47.3398 24.1436 46.6953 25.1494C46.0605 26.165 45.1719 26.9316 44.0293 27.4492C42.8867 27.9766 41.5586 28.2402 40.0449 28.2402C39.3809 28.2402 38.6777 28.1523 37.9355 27.9766C37.2031 27.8008 36.5 27.5273 35.8262 27.1562C35.1621 26.7852 34.6055 26.3164 34.1562 25.75L36.0166 23.2598C36.5049 23.8262 37.0713 24.2656 37.7158 24.5781C38.3604 24.9004 39.0732 25.0615 39.8545 25.0615C40.6162 25.0615 41.2607 24.9199 41.7881 24.6367C42.3154 24.3633 42.7207 23.958 43.0039 23.4209C43.2871 22.8936 43.4287 22.2539 43.4287 21.502V9.8125L43.8389 6.15039ZM33.1748 14.2656V13.958C33.1748 12.7471 33.3213 11.6484 33.6143 10.6621C33.917 9.66602 34.3418 8.81152 34.8887 8.09863C35.4453 7.38574 36.1191 6.83398 36.9102 6.44336C37.7012 6.05273 38.5947 5.85742 39.5908 5.85742C40.6455 5.85742 41.5293 6.05273 42.2422 6.44336C42.9551 6.83398 43.541 7.39062 44 8.11328C44.459 8.82617 44.8154 9.6709 45.0693 10.6475C45.333 11.6143 45.5381 12.6738 45.6846 13.8262V14.5C45.5381 15.6035 45.3184 16.6289 45.0254 17.5762C44.7324 18.5234 44.3467 19.3535 43.8682 20.0664C43.3896 20.7695 42.7939 21.3164 42.0811 21.707C41.3779 22.0977 40.5381 22.293 39.5615 22.293C38.585 22.293 37.7012 22.0928 36.9102 21.6924C36.1289 21.292 35.46 20.7305 34.9033 20.0078C34.3467 19.2852 33.917 18.4355 33.6143 17.459C33.3213 16.4824 33.1748 15.418 33.1748 14.2656ZM37.3936 13.958V14.2656C37.3936 14.9199 37.457 15.5303 37.584 16.0967C37.7109 16.6631 37.9062 17.166 38.1699 17.6055C38.4434 18.0352 38.7803 18.3721 39.1807 18.6162C39.5908 18.8506 40.0742 18.9678 40.6309 18.9678C41.4023 18.9678 42.0322 18.8066 42.5205 18.4844C43.0088 18.1523 43.375 17.6982 43.6191 17.1221C43.8633 16.5459 44.0049 15.8818 44.0439 15.1299V13.2109C44.0244 12.5957 43.9414 12.0439 43.7949 11.5557C43.6484 11.0576 43.4434 10.6328 43.1797 10.2812C42.916 9.92969 42.5742 9.65625 42.1543 9.46094C41.7344 9.26562 41.2363 9.16797 40.6602 9.16797C40.1035 9.16797 39.6201 9.29492 39.21 9.54883C38.8096 9.79297 38.4727 10.1299 38.1992 10.5596C37.9355 10.9893 37.7354 11.4971 37.5986 12.083C37.4619 12.6592 37.3936 13.2842 37.3936 13.958ZM50.2695 14.2363V13.9287C50.2695 12.7666 50.4355 11.6973 50.7676 10.7207C51.0996 9.73438 51.583 8.87988 52.2178 8.15723C52.8525 7.43457 53.6338 6.87305 54.5615 6.47266C55.4893 6.0625 56.5537 5.85742 57.7549 5.85742C58.9561 5.85742 60.0254 6.0625 60.9629 6.47266C61.9004 6.87305 62.6865 7.43457 63.3213 8.15723C63.9658 8.87988 64.4541 9.73438 64.7861 10.7207C65.1182 11.6973 65.2842 12.7666 65.2842 13.9287V14.2363C65.2842 15.3887 65.1182 16.458 64.7861 17.4443C64.4541 18.4209 63.9658 19.2754 63.3213 20.0078C62.6865 20.7305 61.9053 21.292 60.9775 21.6924C60.0498 22.0928 58.9854 22.293 57.7842 22.293C56.583 22.293 55.5137 22.0928 54.5762 21.6924C53.6484 21.292 52.8623 20.7305 52.2178 20.0078C51.583 19.2754 51.0996 18.4209 50.7676 17.4443C50.4355 16.458 50.2695 15.3887 50.2695 14.2363ZM54.4883 13.9287V14.2363C54.4883 14.9004 54.5469 15.5205 54.6641 16.0967C54.7812 16.6729 54.9668 17.1807 55.2207 17.6201C55.4844 18.0498 55.8262 18.3867 56.2461 18.6309C56.666 18.875 57.1787 18.9971 57.7842 18.9971C58.3701 18.9971 58.873 18.875 59.293 18.6309C59.7129 18.3867 60.0498 18.0498 60.3037 17.6201C60.5576 17.1807 60.7432 16.6729 60.8604 16.0967C60.9873 15.5205 61.0508 14.9004 61.0508 14.2363V13.9287C61.0508 13.2842 60.9873 12.6787 60.8604 12.1123C60.7432 11.5361 60.5527 11.0283 60.2891 10.5889C60.0352 10.1396 59.6982 9.78809 59.2783 9.53418C58.8584 9.28027 58.3506 9.15332 57.7549 9.15332C57.1592 9.15332 56.6514 9.28027 56.2314 9.53418C55.8213 9.78809 55.4844 10.1396 55.2207 10.5889C54.9668 11.0283 54.7812 11.5361 54.6641 12.1123C54.5469 12.6787 54.4883 13.2842 54.4883 13.9287Z" fill="#3751FE" />
                    </svg>

                </Box>
                <Box className="login-page__left__form" mt={24} mb={"auto"}>
                    <Stack spacing={15}>
                        <Heading fontWeight={600}>Login</Heading>
                        <Box mb={15}>
                            Welcome back! Please login to your account.
                        </Box>
                        <Box>
                            <form>
                                <Stack spacing={6}>
                                    {/* Show error message if login fails */}
                                    {loginError && (
                                        <Box color="red" textAlign="center">
                                            {loginError}
                                        </Box>
                                    )}
                                    <FormControl variant="floating" isInvalid={emailError?.length > 0}>
                                        <InputGroup flexDirection="column">
                                            <Input
                                                className='outline'
                                                type="email" borderRadius={4}
                                                onChange={(e) => {
                                                    setEmail(e.target.value);
                                                    setEmailError('');
                                                    setLoginError('');
                                                }} />
                                            <FormLabel fontWeight={400}>Email</FormLabel>
                                            <FormErrorMessage>{emailError}</FormErrorMessage>
                                        </InputGroup>
                                    </FormControl>
                                    <FormControl variant="floating" isInvalid={passwordError?.length > 0}>
                                        <InputGroup flexDirection="column">
                                            <Input type={show ? 'text' : 'password'} borderRadius={4}
                                                onChange={(e) => {
                                                    setPassword(e.target.value);
                                                    setPasswordError('');
                                                    setLoginError('');
                                                }} />
                                            <FormLabel fontWeight={400}>Password</FormLabel>
                                            <InputRightElement>
                                                <Button size='sm' bg={"white"} _hover={{ background: "white" }}
                                                    onClick={handleClick}>
                                                    {show ? <ViewIcon /> : <ViewOffIcon />}
                                                </Button>
                                            </InputRightElement>
                                            <FormErrorMessage>{passwordError}</FormErrorMessage>
                                        </InputGroup>
                                    </FormControl>
                                    <FormControl>
                                        <Flex flexDirection="row" justifyContent="space-between" mb={5}>
                                            <Checkbox className='bg-white'>Remember me</Checkbox>
                                            <Box>
                                                <Button variant="link" colorScheme="black" _hover={{ textDecoration: "none" }}>
                                                    Forgot password?
                                                </Button>
                                            </Box>
                                        </Flex>
                                    </FormControl>
                                    <FormControl className='flex justify-start items-center'>
                                        <button className='w-[200px] h-[50px] flex justify-center items-center p-4 mr-10 bg-[#3751FE] text-[#fff]'
                                            onClick={(e) => handleSubmit(e)}>
                                            Login
                                        </button>
                                        <Link to="/sign-up">
                                            <div className='w-[200px] h-[50px] flex justify-center items-center p-4 mr-5 border border-[#3751FE] bg-white'>
                                                SignUp
                                            </div>
                                        </Link>
                                    </FormControl>
                                    <FormControl textAlign="center">
                                        <Flex
                                            className='justify-between items-center mt-10'
                                            width="full">
                                            <Box padding="0 15px" position="relative" zIndex={1} width="fit-content"
                                                color="gray" fontSize={14} bg="white">
                                                or login with
                                            </Box>
                                            <Button padding="0 15px" position="relative" zIndex={1} width="fit-content"
                                                color="#3751FE"
                                                fontSize={14}
                                                bg="white"
                                                className='!font-bold'
                                            >
                                                Google
                                            </Button>
                                        </Flex>
                                    </FormControl>
                                </Stack>
                            </form>
                        </Box>
                    </Stack>
                </Box>

            </Box>
            <Box
                backgroundColor={"#E5E5E5"}
                p={20}
                className="login-page__right" h="calc(100%)" w="calc(100% - 100px)">
                <div className='flex gap-10'>
                    <NavLink to="/vendor/login" className="login-page__right__vendor">Home</NavLink>
                    <NavLink to="/vendor/login" className="login-page__right__vendor">About us</NavLink>
                    <NavLink to="/vendor/login" className="login-page__right__vendor">Blog</NavLink>
                    <NavLink to="/vendor/login" className="login-page__right__vendor">Pricing</NavLink>
                </div>
                <div className='w-full h-full flex justify-center items-center'>
                    <img src={LoginImg} alt="login-img" style={{ width: "100%" }} />
                </div>
            </Box>
        </Flex>
    );
}

export default Login;