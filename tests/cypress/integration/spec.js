// beforeEach('Launch site', () => {
//     cy.visit('https://127.0.0.1:5000');
// });

// it('Testing form', () => {
//     const imagePath = "pic1.png";
//     cy.get('#image_input').attachFile(imagePath);
//     const videoPath = "test_video.mp4";
//     cy.get('#video_input').attachFile(videoPath);

//     cy.get('#submit_btn').click();

//     cy.get('#uploaded-files').contains(imagePath, videoPath);
// });

// // it('Testing picture uploading', () => {
// //     cy.fixture('pic1.png').then(fileContent => {
// //         cy.get('#image_input').attachFile({
// //             fileContent: fileContent.toString(),
// //             fileName: 'pic1.png',
// //             mimeType: 'image/png'
// //         });
// //     });
// // });