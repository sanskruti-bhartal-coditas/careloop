package org.project.javabackend.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.project.javabackend.dto.request.PatientProfileRequestDto;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.entity.PatientDetails;
import org.project.javabackend.entity.User;
import org.project.javabackend.exception.CustomException;
import org.project.javabackend.repo.PatientDetailsRepo;
import org.project.javabackend.repo.UserRepo;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
@Transactional
public class PatientService {

    private final PatientDetailsRepo patientDetailsRepo;
    private final UserRepo userRepo;
    private final UserService userService;


    public GenericResponse addProfile(PatientProfileRequestDto profileRequestDto) {

        User user = userRepo.findById(profileRequestDto.id()).orElseThrow(()-> new CustomException(HttpStatus.BAD_REQUEST,"user not found"));

        PatientDetails patientDetails = patientDetailsRepo.findByUser_Id(profileRequestDto.id());

        if(patientDetails == null){
            patientDetails = PatientDetails.builder()
                    .firstName(profileRequestDto.firstName())
                    .lastName(profileRequestDto.lastName())
                    .phone(profileRequestDto.phone())
                    .age(profileRequestDto.age())
                    .height(profileRequestDto.height())
                    .weight(profileRequestDto.weight())
                    .user(user)
                    .build();
        }
        else {
            if(patientDetails.getFirstName()==null) patientDetails.setFirstName(profileRequestDto.firstName());
            if(patientDetails.getLastName()==null) patientDetails.setLastName(profileRequestDto.lastName());
            if(patientDetails.getPhone()==null) patientDetails.setPhone(profileRequestDto.phone());
            if(patientDetails.getAge()==null) patientDetails.setAge(profileRequestDto.age());
            if(patientDetails.getHeight()==null) patientDetails.setHeight(profileRequestDto.height());
            if(patientDetails.getWeight()==null) patientDetails.setWeight(profileRequestDto.weight());
        }


        patientDetailsRepo.save(patientDetails);
        return new GenericResponse(HttpStatus.OK,"profile updated successfully");
    }
}
